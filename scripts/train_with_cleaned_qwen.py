"""
使用清洗后的千问数据训练 TextCNN
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from torch.utils.data import DataLoader
from src.router.textcnn_model import TextCNNLite
from src.router.train_router import Trainer, TextDataset
from src.router.category_config import CategoryConfig


def load_and_merge_data():
    """合并原始数据和清洗后的千问数据"""
    data_dir = Path("data/processed")

    # 加载原始数据
    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        original_train = json.load(f)

    with open(data_dir / "val_data.json", "r", encoding="utf-8") as f:
        original_val = json.load(f)

    # 加载清洗后的千问数据
    with open(data_dir / "qwen_samples_cleaned.json", "r", encoding="utf-8") as f:
        qwen_cleaned = json.load(f)

    print(f"原始训练集: {len(original_train)}")
    print(f"原始验证集: {len(original_val)}")
    print(f"千问清洗数据: {len(qwen_cleaned)}")

    # 将千问数据合并到训练集
    merged_train = original_train + qwen_cleaned

    # 去重
    unique_texts = set()
    final_train = []
    for item in merged_train:
        if item["text"] not in unique_texts:
            unique_texts.add(item["text"])
            final_train.append(item)

    print(f"合并后训练集: {len(final_train)} (去重后)")

    return final_train, original_val


def split_train_val(train_data, val_ratio=0.15):
    """从训练集分出验证集"""
    import random

    # 按类别分组
    by_category = {}
    for item in train_data:
        cat = item.get("category_name", item.get("category", ""))
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)

    # 分层抽样
    new_train = []
    new_val = []

    for cat, items in by_category.items():
        random.shuffle(items)
        split_idx = int(len(items) * (1 - val_ratio))

        new_train.extend(items[:split_idx])
        new_val.extend(items[split_idx:])

    print(f"重新划分后 - 训练集: {len(new_train)}, 验证集: {len(new_val)}")

    return new_train, new_val


def main():
    print("=" * 70)
    print("使用清洗后的千问数据训练 TextCNN")
    print("=" * 70)

    # 加载和合并数据
    train_data, val_data = load_and_merge_data()

    # 重新划分训练/验证集（将千问数据也分配到验证集）
    train_data, val_data = split_train_val(train_data, val_ratio=0.15)

    # 创建词汇表
    vocab = CategoryConfig.create_vocabulary()
    print(f"词汇表大小: {len(vocab)}")

    # 创建数据集
    train_dataset = TextDataset(train_data, vocab, max_len=64)
    val_dataset = TextDataset(val_data, vocab, max_len=64)

    # 创建数据加载器
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
    print(f"使用设备: {device}")

    # 训练
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
        save_dir=Path("data/models/router_cleaned")
    )

    print("\n训练完成!")
    print(f"最佳验证准确率: {trainer.best_val_acc:.4f}")


if __name__ == "__main__":
    main()
