"""
训练路由模型脚本
运行: python scripts/train_router.py
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import torch
from src.router.train_router import load_data, TextDataset, Trainer
from src.router.category_config import CategoryConfig
from src.router.textcnn_model import TextCNNLite
from torch.utils.data import DataLoader


def main():
    print("=" * 60)
    print("训练路由分类模型")
    print("=" * 60)

    # 设备
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"设备: {device}")

    # 加载数据
    train_data, val_data, _ = load_data()

    if not train_data:
        print("错误: 没有加载到训练数据")
        print("提示: 按顺序运行以下脚本:")
        print("  1. python scripts/parse_skills.py")
        print("  2. python scripts/generate_queries.py")
        print("  3. python scripts/process_data.py")
        return

    # 创建词汇表
    vocab = CategoryConfig.create_vocabulary()
    vocab_size = len(vocab)
    num_classes = len(CategoryConfig.CATEGORIES)

    # 创建数据集
    train_dataset = TextDataset(train_data, vocab, max_len=64)
    val_dataset = TextDataset(val_data, vocab, max_len=64)

    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    # 创建模型
    model = TextCNNLite(vocab_size, num_classes=num_classes)

    print("\n模型信息:")
    info = model.get_model_info()
    print(f"  总参数: {info['total_params']:,}")
    print(f"  模型大小: {info['model_size_mb']:.2f} MB")

    # 创建训练器
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device
    )

    # 训练
    history = trainer.train(
        num_epochs=50,
        early_stopping=10
    )

    print("\n训练完成!")


if __name__ == "__main__":
    main()
