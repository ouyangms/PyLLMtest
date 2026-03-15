"""
在清洗后的数据上训练模型
使用清洗后的训练集（去除无效样本）+ 小样本类别增强数据
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


def main():
    print("=" * 70)
    print("在清洗后的数据上训练 TextCNN")
    print("=" * 70)

    # 加载清洗并增强后的训练数据
    data_dir = Path("data/processed")

    with open(data_dir / "train_data_clean_aug.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open(data_dir / "val_data_clean.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    print(f"\n训练集: {len(train_data)}")
    print(f"验证集: {len(val_data)}")

    # 统计类别分布
    from collections import Counter
    train_dist = Counter([item.get("category_name", item.get("category", "")) for item in train_data])
    print("\n训练集类别分布:")
    for cat, count in sorted(train_dist.items()):
        print(f"  {cat:20s}: {count:4d}")

    # 创建词汇表和数据集
    vocab = CategoryConfig.create_vocabulary()

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
        save_dir=Path("data/models/router_clean_final")
    )

    print("\n训练完成!")
    print(f"最佳验证准确率: {trainer.best_val_acc:.4f}")


if __name__ == "__main__":
    main()
