"""
训练增强版 TextCNN 分类器
- 使用类别权重平衡
- Focal Loss
- 学习率调度
- 数据增强
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router.textcnn_enhanced import TextCNNEnhanced
from src.router.train_router import TextDataset
from src.router.category_config import CategoryConfig


class FocalLoss(nn.Module):
    """
    Focal Loss
    关注难分类样本，减少简单样本的权重

    FL(p_t) = -alpha_t * (1 - p_t)^gamma * log(p_t)

    Args:
        alpha: 类别权重
        gamma: 聚焦参数（越大越关注难样本）
        reduction: 'mean' 或 'sum'
    """

    def __init__(self, alpha: torch.Tensor = None, gamma: float = 2.0, reduction: str = 'mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Args:
            inputs: [batch_size, num_classes] logits
            targets: [batch_size] 类别索引

        Returns:
            loss
        """
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        p_t = torch.exp(-ce_loss)
        focal_loss = (1 - p_t) ** self.gamma * ce_loss

        if self.alpha is not None:
            alpha_t = self.alpha[targets]
            focal_loss = alpha_t * focal_loss

        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss


class CosineAnnealingWarmupScheduler:
    """
    带预热的余弦退火学习率调度器
    """

    def __init__(
        self,
        optimizer: optim.Optimizer,
        warmup_epochs: int,
        max_epochs: int,
        base_lr: float,
        max_lr: float,
        min_lr: float
    ):
        self.optimizer = optimizer
        self.warmup_epochs = warmup_epochs
        self.max_epochs = max_epochs
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.min_lr = min_lr
        self.current_epoch = 0

    def step(self):
        """更新学习率"""
        self.current_epoch += 1

        if self.current_epoch <= self.warmup_epochs:
            # 预热阶段：线性增加
            lr = self.base_lr + (self.max_lr - self.base_lr) * self.current_epoch / self.warmup_epochs
        else:
            # 余弦退火阶段
            progress = (self.current_epoch - self.warmup_epochs) / (self.max_epochs - self.warmup_epochs)
            lr = self.min_lr + 0.5 * (self.max_lr - self.min_lr) * (1 + np.cos(np.pi * progress))

        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr

        return lr

    def get_lr(self):
        """获取当前学习率"""
        return self.optimizer.param_groups[0]['lr']


class EnhancedTrainer:
    """增强版训练器"""

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        device: str = "cuda",
        learning_rate: float = 0.001,
        weight_decay: float = 1e-4,
        use_focal_loss: bool = True,
        use_class_weights: bool = True
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device

        # 计算类别权重
        if use_class_weights:
            class_weights = self._compute_class_weights()
            print(f"类别权重: {class_weights}")
            class_weights = class_weights.to(device)
        else:
            class_weights = None

        # 损失函数
        if use_focal_loss:
            self.criterion = FocalLoss(alpha=class_weights, gamma=2.0)
            print("使用 Focal Loss")
        else:
            self.criterion = nn.CrossEntropyLoss(weight=class_weights)
            print("使用 CrossEntropyLoss")

        # 优化器
        self.optimizer = optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
            betas=(0.9, 0.999)
        )

        # 训练历史
        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
            "lr": []
        }

        # 最佳模型
        self.best_val_acc = 0.0
        self.best_epoch = 0

    def _compute_class_weights(self) -> torch.Tensor:
        """计算类别权重（逆频率）"""
        # 统计每个类别的样本数
        class_counts = torch.zeros(len(CategoryConfig.CATEGORIES))
        for _, labels in self.train_loader:
            for label in labels:
                class_counts[label] += 1

        # 计算权重（逆频率）
        total_samples = class_counts.sum()
        class_weights = total_samples / (len(CategoryConfig.CATEGORIES) * class_counts)

        # 归一化
        class_weights = class_weights / class_weights.sum() * len(CategoryConfig.CATEGORIES)

        return class_weights

    def train_epoch(self) -> Tuple[float, float]:
        """训练一个 epoch"""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        pbar = tqdm(self.train_loader, desc="Training")
        for indices, labels in pbar:
            indices = indices.to(self.device)
            labels = labels.to(self.device)

            # 前向传播
            self.optimizer.zero_grad()
            outputs = self.model(indices)
            loss = self.criterion(outputs, labels)

            # 反向传播
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()

            # 统计
            total_loss += loss.item() * indices.size(0)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

            # 更新进度条
            pbar.set_postfix({
                "loss": f"{loss.item():.4f}",
                "acc": f"{correct / total:.4f}"
            })

        avg_loss = total_loss / total
        accuracy = correct / total
        return avg_loss, accuracy

    def validate(self) -> Tuple[float, float]:
        """验证模型"""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for indices, labels in tqdm(self.val_loader, desc="Validating"):
                indices = indices.to(self.device)
                labels = labels.to(self.device)

                # 前向传播
                outputs = self.model(indices)
                loss = self.criterion(outputs, labels)

                # 统计
                total_loss += loss.item() * indices.size(0)
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

        avg_loss = total_loss / total
        accuracy = correct / total
        return avg_loss, accuracy

    def train(
        self,
        num_epochs: int = 100,
        early_stopping: int = 15,
        save_dir: str = None,
        warmup_epochs: int = 5
    ) -> Dict:
        """
        训练模型

        Args:
            num_epochs: 训练轮数
            early_stopping: 早停轮数
            save_dir: 保存目录
            warmup_epochs: 预热轮数
        """
        if save_dir is None:
            save_dir = Path(__file__).parent.parent / "data" / "models" / "router_enhanced"
        else:
            save_dir = Path(save_dir)

        save_dir.mkdir(parents=True, exist_ok=True)

        print("=" * 60)
        print("开始训练增强版模型")
        print("=" * 60)
        print(f"设备: {self.device}")
        print(f"训练集: {len(self.train_loader.dataset)} 样本")
        print(f"验证集: {len(self.val_loader.dataset)} 样本")
        print(f"Epochs: {num_epochs}")
        print(f"早停: {early_stopping}")
        print("=" * 60)

        # 学习率调度器
        scheduler = CosineAnnealingWarmupScheduler(
            self.optimizer,
            warmup_epochs=warmup_epochs,
            max_epochs=num_epochs,
            base_lr=0.0001,
            max_lr=0.001,
            min_lr=0.00001
        )

        no_improve = 0
        start_time = time.time()

        for epoch in range(1, num_epochs + 1):
            epoch_start = time.time()

            # 更新学习率
            lr = scheduler.step()

            # 训练
            train_loss, train_acc = self.train_epoch()

            # 验证
            val_loss, val_acc = self.validate()

            # 记录历史
            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)
            self.history["lr"].append(lr)

            # 打印信息
            epoch_time = time.time() - epoch_start
            print(f"\nEpoch {epoch}/{num_epochs} ({epoch_time:.1f}s)")
            print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            print(f"  LR: {lr:.6f}")

            # 保存检查点
            if epoch % 10 == 0:
                checkpoint_path = save_dir / f"checkpoint_epoch_{epoch}.pth"
                torch.save(self.model.state_dict(), checkpoint_path)
                print(f"  [SAVE] 检查点已保存")

            # 保存最佳模型
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                self.best_epoch = epoch
                no_improve = 0

                best_path = save_dir / "best_model.pth"
                torch.save(self.model.state_dict(), best_path)
                print(f"  [BEST] 模型已保存 (Acc: {val_acc:.4f})")
            else:
                no_improve += 1
                print(f"  无改善: {no_improve}/{early_stopping}")

            # 早停
            if no_improve >= early_stopping:
                print(f"\n早停触发，停止训练")
                break

        total_time = time.time() - start_time
        print("=" * 60)
        print("训练完成")
        print("=" * 60)
        print(f"总时间: {total_time / 60:.1f} 分钟")
        print(f"最佳 Epoch: {self.best_epoch}")
        print(f"最佳验证准确率: {self.best_val_acc:.4f}")
        print(f"模型已保存: {save_dir / 'best_model.pth'}")

        return self.history


def load_data(data_dir: str = None, suffix: str = "") -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """加载数据"""
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data" / "processed"
    else:
        data_dir = Path(data_dir)

    print(f"加载数据: {data_dir}")

    train_file = f"train_data{suffix}.json" if suffix else "train_data.json"
    val_file = f"val_data{suffix}.json" if suffix else "val_data.json"
    test_file = f"test_data{suffix}.json" if suffix else "test_data.json"

    try:
        with open(data_dir / train_file, 'r', encoding='utf-8') as f:
            train_data = json.load(f)

        with open(data_dir / val_file, 'r', encoding='utf-8') as f:
            val_data = json.load(f)

        with open(data_dir / test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)

        print(f"  训练集: {len(train_data)}")
        print(f"  验证集: {len(val_data)}")
        print(f"  测试集: {len(test_data)}")

        return train_data, val_data, test_data

    except FileNotFoundError as e:
        print(f"未找到数据文件: {e}")
        raise


def main():
    """主函数"""
    import argparse
    import torch.nn.functional as F

    parser = argparse.ArgumentParser(description="训练增强版路由分类器")
    parser.add_argument("--data-dir", type=str, default="data/processed", help="数据目录")
    parser.add_argument("--data-suffix", type=str, default="", help="数据文件后缀")
    parser.add_argument("--output-dir", type=str, default="data/models/router_enhanced", help="输出目录")
    parser.add_argument("--max-len", type=int, default=64, help="最大序列长度")
    parser.add_argument("--batch-size", type=int, default=64, help="批大小")
    parser.add_argument("--num-epochs", type=int, default=100, help="训练轮数")
    parser.add_argument("--learning-rate", type=float, default=0.001, help="学习率")
    parser.add_argument("--early-stopping", type=int, default=15, help="早停轮数")
    parser.add_argument("--warmup-epochs", type=int, default=5, help="预热轮数")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu", help="设备")
    parser.add_argument("--no-focal", action="store_true", help="不使用 Focal Loss")
    parser.add_argument("--no-weights", action="store_true", help="不使用类别权重")

    args = parser.parse_args()

    # 设置随机种子
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(42)

    # 加载数据
    train_data, val_data, test_data = load_data(args.data_dir, args.data_suffix)

    # 创建词汇表
    vocab = CategoryConfig.create_vocabulary()
    vocab_size = len(vocab)
    num_classes = len(CategoryConfig.CATEGORIES)

    print(f"词汇表大小: {vocab_size}")
    print(f"分类数量: {num_classes}")

    # 创建数据集
    train_dataset = TextDataset(train_data, vocab, max_len=args.max_len)
    val_dataset = TextDataset(val_data, vocab, max_len=args.max_len)

    # 创建数据加载器
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=True if args.device == "cuda" else False
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True if args.device == "cuda" else False
    )

    # 创建增强版模型
    model = TextCNNEnhanced(vocab_size, num_classes=num_classes)

    print("\n模型信息:")
    info = model.get_model_info()
    for key, value in info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        elif isinstance(value, bool):
            print(f"  {key}: {'是' if value else '否'}")
        else:
            print(f"  {key}: {value}")

    # 创建训练器
    trainer = EnhancedTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=args.device,
        learning_rate=args.learning_rate,
        use_focal_loss=not args.no_focal,
        use_class_weights=not args.no_weights
    )

    # 训练
    history = trainer.train(
        num_epochs=args.num_epochs,
        early_stopping=args.early_stopping,
        save_dir=args.output_dir,
        warmup_epochs=args.warmup_epochs
    )


if __name__ == "__main__":
    main()
