"""
使用原始数据 + Focal Loss + 类别权重训练模型
专门处理类别不平衡问题
"""

import sys
import json
from pathlib import Path
from collections import Counter

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from src.router.textcnn_focal import TextCNNSmall, FocalLoss
from src.router.train_router import TextDataset
from src.router.category_config import CategoryConfig


def compute_class_weights(train_data, num_classes=13):
    """计算类别权重 - 给予少数类更高权重"""
    # 统计每个类别的样本数
    label_counts = Counter([item["category_id"] for item in train_data])

    total_samples = len(train_data)

    # 计算权重：使用逆频率加权
    # weight = total_samples / (num_classes * class_count)
    weights = []
    for i in range(num_classes):
        count = label_counts.get(i, 1)  # 避免除以0
        weight = total_samples / (num_classes * count)
        weights.append(weight)

    weights = torch.tensor(weights, dtype=torch.float32)

    print("类别权重:")
    for i, w in enumerate(weights):
        cat_name = CategoryConfig.CATEGORIES[i]
        count = label_counts.get(i, 0)
        print(f"  {i:2d} {cat_name:20s}: count={count:4d}, weight={w:.2f}")

    return weights


def train_epoch(model, dataloader, optimizer, criterion, device):
    """训练一个 epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for batch in dataloader:
        indices, labels = batch
        indices, labels = indices.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(indices)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

    return total_loss / len(dataloader), correct / total


def validate(model, dataloader, criterion, device):
    """验证"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for batch in dataloader:
            indices, labels = batch
            indices, labels = indices.to(device), labels.to(device)

            outputs = model(indices)
            loss = criterion(outputs, labels)

            total_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    return total_loss / len(dataloader), correct / total


def main():
    print("=" * 70)
    print("使用 Focal Loss + 类别权重训练 TextCNN")
    print("=" * 70)

    # 加载原始数据
    data_dir = Path("data/processed")

    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open(data_dir / "val_data.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    print(f"\n训练集: {len(train_data)}")
    print(f"验证集: {len(val_data)}")

    # 创建词汇表和数据集
    vocab = CategoryConfig.create_vocabulary()
    print(f"词汇表大小: {len(vocab)}")

    train_dataset = TextDataset(train_data, vocab, max_len=64)
    val_dataset = TextDataset(val_data, vocab, max_len=64)

    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True,
        num_workers=0
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0
    )

    # 计算类别权重
    class_weights = compute_class_weights(train_data, num_classes=13)
    class_weights = class_weights.to("cuda" if torch.cuda.is_available() else "cpu")

    # 创建模型
    model = TextCNNSmall(len(vocab), num_classes=13)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    print(f"\n模型参数量: {model.get_model_info()['total_params']:,}")
    print(f"使用设备: {device}")

    # 使用 Focal Loss
    criterion = FocalLoss(alpha=class_weights, gamma=2.0)

    # 优化器 - 使用 AdamW
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

    # 学习率调度器
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=3
    )

    # 训练
    print("\n" + "=" * 70)
    print("开始训练")
    print("=" * 70)

    best_val_acc = 0
    patience = 15
    no_improve = 0

    for epoch in range(1, 51):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = validate(model, val_loader, criterion, device)

        # 更新学习率
        scheduler.step(val_acc)

        print(f"\nEpoch {epoch}/50")
        print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
        print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")

        # 保存最佳模型
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            no_improve = 0

            save_dir = Path("data/models/router_focal")
            save_dir.mkdir(parents=True, exist_ok=True)

            torch.save(model.state_dict(), save_dir / "best_model.pth")
            print(f"  [BEST] 模型已保存 (Acc: {val_acc:.4f})")
        else:
            no_improve += 1
            print(f"  无提升: {no_improve}/{patience}")

        # 早停
        if no_improve >= patience:
            print(f"\n早停触发，停止训练")
            break

    print("\n训练完成!")
    print(f"最佳验证准确率: {best_val_acc:.4f}")


if __name__ == "__main__":
    main()
