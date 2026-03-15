"""
训练 BERT 路由分类器
"""

import json
import os
import time
from pathlib import Path

import torch
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router.bert_classifier import train_bert, BERTRouter
from src.router.category_config import CategoryConfig


def load_training_data(data_dir: str = "data/processed"):
    """加载训练数据"""
    data_dir = Path(data_dir)

    # 加载路由数据
    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open(data_dir / "val_data.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    return train_data, val_data


def main():
    import argparse

    parser = argparse.ArgumentParser(description="训练 BERT 路由分类器")
    parser.add_argument(
        "--model-name",
        type=str,
        default="huawei-noah/TinyBERT_General_4L_312D",
        help="BERT 模型名称"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/processed",
        help="数据目录"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/models/router_bert",
        help="输出目录"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="训练轮数"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="批次大小"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-5,
        help="学习率"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=64,
        help="最大序列长度"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="设备"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("训练 BERT 路由分类器")
    print("=" * 60)

    # 检查设备
    print(f"\n设备: {args.device}")
    if args.device == "cuda" and torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"显存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    # 加载数据
    print(f"\n加载数据: {args.data_dir}")
    train_data, val_data = load_training_data(args.data_dir)

    print(f"训练样本: {len(train_data)}")
    print(f"验证样本: {len(val_data)}")

    # 检查类别
    num_classes = len(CategoryConfig.CATEGORIES)
    print(f"类别数: {num_classes}")

    # 训练
    start_time = time.time()

    try:
        trainer, model = train_bert(
            train_data=train_data,
            val_data=val_data,
            model_name=args.model_name,
            output_dir=args.output_dir,
            num_epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate,
            max_length=args.max_length,
            early_stopping_patience=2
        )

        elapsed = time.time() - start_time

        print("\n" + "=" * 60)
        print("训练完成")
        print("=" * 60)
        print(f"总耗时: {elapsed:.1f}s ({elapsed/60:.1f} 分钟)")

        # 获取训练历史
        if hasattr(trainer.state, "log_history"):
            history = trainer.state.log_history

            # 找到最佳准确率
            best_accuracy = 0
            for log in history:
                if "eval_accuracy" in log:
                    best_accuracy = max(best_accuracy, log["eval_accuracy"])

            print(f"最佳验证准确率: {best_accuracy:.4f}")

    except Exception as e:
        print(f"\n训练失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
