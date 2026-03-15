"""
路由分类器训练脚本
训练 TextCNN 模型用于技能分类
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

from .textcnn_model import TextCNN, TextCNNLite, create_model
from ..router.category_config import CategoryConfig


class TextDataset(Dataset):
    """文本数据集"""

    def __init__(self, data: List[Dict], vocab: Dict[str, int], max_len: int = 64):
        """
        初始化数据集

        Args:
            data: 数据列表，每项包含 {text, category_id}
            vocab: 词汇表
            max_len: 最大序列长度
        """
        self.data = data
        self.vocab = vocab
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        item = self.data[idx]
        text = item["text"]
        label = item["category_id"]

        # 文本编码
        indices = self._encode_text(text)
        return indices, label

    def _encode_text(self, text: str) -> torch.Tensor:
        """
        将文本编码为索引序列

        Args:
            text: 输入文本

        Returns:
            索引张量
        """
        # 字符级编码
        indices = []
        for char in text[:self.max_len]:
            idx = self.vocab.get(char, self.vocab.get("<UNK>", 1))
            indices.append(idx)

        # 填充或截断
        if len(indices) < self.max_len:
            indices.extend([self.vocab.get("<PAD>", 0)] * (self.max_len - len(indices)))

        return torch.tensor(indices, dtype=torch.long)


class Trainer:
    """训练器"""

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        device: str = "cuda",
        learning_rate: float = 0.001,
        weight_decay: float = 1e-4
    ):
        """
        初始化训练器

        Args:
            model: 模型
            train_loader: 训练数据加载器
            val_loader: 验证数据加载器
            device: 设备 (cuda/cpu)
            learning_rate: 学习率
            weight_decay: 权重衰减
        """
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device

        # 损失函数
        self.criterion = nn.CrossEntropyLoss()

        # 优化器
        self.optimizer = optim.Adam(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )

        # 学习率调度器
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='min',
            factor=0.5,
            patience=3
        )

        # 训练历史
        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": []
        }

        # 最佳模型
        self.best_val_acc = 0.0
        self.best_epoch = 0

    def train_epoch(self) -> Tuple[float, float]:
        """
        训练一个 epoch

        Returns:
            (loss, accuracy)
        """
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
        """
        验证模型

        Returns:
            (loss, accuracy)
        """
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
        num_epochs: int = 50,
        early_stopping: int = 10,
        save_dir: str = None
    ) -> Dict:
        """
        训练模型

        Args:
            num_epochs: 训练轮数
            early_stopping: 早停轮数
            save_dir: 保存目录

        Returns:
            训练历史
        """
        if save_dir is None:
            save_dir = Path(__file__).parent.parent.parent / "data" / "models" / "router"
        else:
            save_dir = Path(save_dir)

        save_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_dir = save_dir / "checkpoints"
        checkpoint_dir.mkdir(exist_ok=True)

        print("=" * 60)
        print("开始训练")
        print("=" * 60)
        print(f"设备: {self.device}")
        print(f"训练集: {len(self.train_loader.dataset)} 样本")
        print(f"验证集: {len(self.val_loader.dataset)} 样本")
        print(f"Epochs: {num_epochs}")
        print(f"早停: {early_stopping}")
        print("=" * 60)

        no_improve = 0
        start_time = time.time()

        for epoch in range(1, num_epochs + 1):
            epoch_start = time.time()

            # 训练
            train_loss, train_acc = self.train_epoch()

            # 验证
            val_loss, val_acc = self.validate()

            # 学习率调度
            self.scheduler.step(val_loss)

            # 记录历史
            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)

            # 打印信息
            epoch_time = time.time() - epoch_start
            print(f"\nEpoch {epoch}/{num_epochs} ({epoch_time:.1f}s)")
            print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            print(f"  LR: {self.optimizer.param_groups[0]['lr']:.6f}")

            # 保存检查点
            if (epoch) % 5 == 0:
                checkpoint_path = checkpoint_dir / f"checkpoint_epoch_{epoch}.pth"
                torch.save(self.model.state_dict(), checkpoint_path)
                print(f"  [SAVE] 检查点已保存: {checkpoint_path}")

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


def load_data(data_dir: str = None) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    加载训练数据

    Args:
        data_dir: 数据目录

    Returns:
        (train_data, val_data, test_data)
    """
    if data_dir is None:
        data_dir = Path(__file__).parent.parent.parent / "data" / "processed"
    else:
        data_dir = Path(data_dir)

    print(f"加载数据: {data_dir}")

    with open(data_dir / "train_data.json", 'r', encoding='utf-8') as f:
        train_data = json.load(f)

    with open(data_dir / "val_data.json", 'r', encoding='utf-8') as f:
        val_data = json.load(f)

    with open(data_dir / "test_data.json", 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    print(f"  训练集: {len(train_data)}")
    print(f"  验证集: {len(val_data)}")
    print(f"  测试集: {len(test_data)}")

    return train_data, val_data, test_data


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="训练路由分类器")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/processed",
        help="数据目录"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/models/router",
        help="输出目录"
    )
    parser.add_argument(
        "--max-len",
        type=int,
        default=64,
        help="最大序列长度"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="批大小"
    )
    parser.add_argument(
        "--num-epochs",
        type=int,
        default=50,
        help="训练轮数"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.001,
        help="学习率"
    )
    parser.add_argument(
        "--early-stopping",
        type=int,
        default=10,
        help="早停轮数"
    )
    parser.add_argument(
        "--lite",
        action="store_true",
        help="使用轻量版模型"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="设备 (cuda/cpu)"
    )

    args = parser.parse_args()

    # 设置随机种子
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(42)

    # 加载数据
    train_data, val_data, test_data = load_data(args.data_dir)

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

    # 创建模型
    model_class = TextCNNLite if args.lite else TextCNN
    model = model_class(vocab_size, num_classes=num_classes)

    print("\n模型信息:")
    info = model.get_model_info()
    for key, value in info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    # 创建训练器
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=args.device,
        learning_rate=args.learning_rate
    )

    # 训练
    history = trainer.train(
        num_epochs=args.num_epochs,
        early_stopping=args.early_stopping,
        save_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
