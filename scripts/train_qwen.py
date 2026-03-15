"""
使用千问增强数据训练 TextCNN
"""

import sys
sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.router.train_router import Trainer, TextDataset, load_data
from src.router.category_config import CategoryConfig
from src.router.textcnn_model import TextCNNLite
import torch
import json
from pathlib import Path


def main():
    # 加载千问增强数据
    data_dir = Path("data/processed")

    with open(data_dir / "train_data_qwen.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open(data_dir / "val_data_qwen.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    print(f"训练集: {len(train_data)}")
    print(f"验证集: {len(val_data)}")

    # 创建词汇表和数据集
    vocab = CategoryConfig.create_vocabulary()

    train_dataset = TextDataset(train_data, vocab, max_len=64)
    val_dataset = TextDataset(val_data, vocab, max_len=64)

    # 创建数据加载器
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True,
        num_workers=0
    )

    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0
    )

    # 创建模型
    model = TextCNNLite(len(vocab), num_classes=13)
    device = "cuda" if torch.cuda.is_available() else "cpu"

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
        save_dir=Path("data/models/router_qwen")
    )

    print("\n训练完成!")
    print(f"最佳验证准确率: {trainer.best_val_acc:.4f}")


if __name__ == "__main__":
    main()
