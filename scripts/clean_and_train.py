"""
清洗原始数据并训练
去除重复样本，使用高质量数据
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from torch.utils.data import DataLoader
from src.router.textcnn_model import TextCNNLite
from src.router.train_router import TextDataset
from src.router.category_config import CategoryConfig


def clean_data(data):
    """清洗数据：去重"""
    seen_texts = set()
    cleaned_data = []

    for item in data:
        text = item["text"].strip()

        # 跳过太短的文本
        if len(text) <= 1:
            continue

        # 去重
        if text not in seen_texts:
            seen_texts.add(text)
            cleaned_data.append(item)

    return cleaned_data


def balance_data(data, samples_per_category=100):
    """平衡数据 - 限制每个类别的样本数"""
    # 按类别分组
    by_category = defaultdict(list)
    for item in data:
        cat = item.get("category_name", item.get("category", ""))
        by_category[cat].append(item)

    balanced_data = []
    import random

    for cat, items in by_category.items():
        # 如果样本数超过目标，随机采样
        if len(items) > samples_per_category:
            items = random.sample(items, samples_per_category)
        balanced_data.extend(items)

    return balanced_data


def main():
    print("=" * 70)
    print("清洗数据并训练")
    print("=" * 70)

    # 加载数据
    data_dir = Path("data/processed")

    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open(data_dir / "val_data.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    with open(data_dir / "test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    print(f"\n原始数据:")
    print(f"  训练集: {len(train_data)}")
    print(f"  验证集: {len(val_data)}")
    print(f"  测试集: {len(test_data)}")

    # 清洗训练数据
    train_cleaned = clean_data(train_data)
    val_cleaned = clean_data(val_data)

    print(f"\n清洗后 (去重):")
    print(f"  训练集: {len(train_cleaned)} (去除 {len(train_data) - len(train_cleaned)} 个重复)")
    print(f"  验证集: {len(val_cleaned)} (去除 {len(val_data) - len(val_cleaned)} 个重复)")

    # 检查类别分布
    from collections import Counter
    train_dist = Counter([item.get("category_name", item.get("category", "")) for item in train_cleaned])
    print(f"\n训练集类别分布:")
    for cat, count in sorted(train_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:4d}")

    # 平衡训练数据（限制每个类别最多 150 个样本）
    train_balanced = balance_data(train_cleaned, samples_per_category=150)
    print(f"\n平衡后训练集: {len(train_balanced)}")

    # 创建词汇表和数据集
    vocab = CategoryConfig.create_vocabulary()

    train_dataset = TextDataset(train_balanced, vocab, max_len=64)
    val_dataset = TextDataset(val_cleaned, vocab, max_len=64)

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

    # 创建模型
    model = TextCNNLite(len(vocab), num_classes=13)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    print(f"\n模型参数量: {model.get_model_info()['total_params']:,}")
    print(f"使用设备: {device}")

    # 训练
    from src.router.train_router import Trainer

    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        learning_rate=0.001
    )

    history = trainer.train(
        num_epochs=50,
        early_stopping=10,
        save_dir=Path("data/models/router_clean")
    )

    print("\n训练完成!")
    print(f"最佳验证准确率: {trainer.best_val_acc:.4f}")


if __name__ == "__main__":
    main()
