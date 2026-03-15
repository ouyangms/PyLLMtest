"""
混合训练：清洗数据 + 原始数据
让模型既能识别清晰样本，也能处理模糊样本
"""

import sys
import json
from pathlib import Path
from collections import Counter

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from torch.utils.data import DataLoader
from src.router.textcnn_model import TextCNNLite
from src.router.train_router import Trainer, TextDataset
from src.router.category_config import CategoryConfig


def main():
    print("=" * 70)
    print("混合训练：清洗数据 + 原始数据")
    print("=" * 70)

    data_dir = Path("data/processed")

    # 加载数据
    with open(data_dir / "train_data_clean_aug.json", "r", encoding="utf-8") as f:
        train_clean = json.load(f)

    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        train_original = json.load(f)

    with open(data_dir / "val_data.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    print(f"\n数据集大小:")
    print(f"  清洗后训练集: {len(train_clean)}")
    print(f"  原始训练集: {len(train_original)}")
    print(f"  验证集: {len(val_data)}")

    # 策略：混合数据，但给予清洗数据更高权重
    # 方案1：重复清洗数据多次
    train_clean_repeated = train_clean * 2  # 重复2次
    train_hybrid = train_clean_repeated + train_original

    print(f"\n混合策略:")
    print(f"  清洗数据重复: 2倍")
    print(f"  混合后训练集: {len(train_hybrid)}")

    # 统计类别分布
    hybrid_dist = Counter([item.get("category_name", item.get("category", "")) for item in train_hybrid])
    print("\n混合后类别分布:")
    for cat, count in sorted(hybrid_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:4d}")

    # 创建词汇表和数据集
    vocab = CategoryConfig.create_vocabulary()

    train_dataset = TextDataset(train_hybrid, vocab, max_len=64)
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

    # 创建模型
    model = TextCNNLite(len(vocab), num_classes=13)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    print(f"\n模型参数量: {model.get_model_info()['total_params']:,}")
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
        save_dir=Path("data/models/router_hybrid")
    )

    print("\n训练完成!")
    print(f"最佳验证准确率: {trainer.best_val_acc:.4f}")


if __name__ == "__main__":
    main()
