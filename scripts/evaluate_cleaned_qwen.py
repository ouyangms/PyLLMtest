"""
评估清洗后千问数据训练的模型
"""

import json
import sys
from pathlib import Path
import torch

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig


def evaluate_model(model_path, test_data_path, device="cuda"):
    """评估模型"""
    with open(test_data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    vocab = CategoryConfig.create_vocabulary()

    model = TextCNNLite(len(vocab), num_classes=13)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    correct = 0
    batch_size = 128

    with torch.no_grad():
        for i in range(0, len(test_data), batch_size):
            batch_end = min(i + batch_size, len(test_data))
            batch_data = test_data[i:batch_end]

            indices_list = []
            for item in batch_data:
                indices = []
                for char in item["text"][:64]:
                    idx = vocab.get(char, vocab.get("<UNK>", 1))
                    indices.append(idx)

                if len(indices) < 64:
                    indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

                indices_list.append(indices)

            indices_tensor = torch.tensor(indices_list, dtype=torch.long).to(device)
            labels_tensor = torch.tensor([item["category_id"] for item in batch_data], dtype=torch.long).to(device)

            outputs = model(indices_tensor)
            _, predicted = torch.max(outputs, 1)

            correct += (predicted == labels_tensor).sum().item()

    accuracy = correct / len(test_data)
    return accuracy, len(test_data)


def main():
    print("=" * 70)
    print("模型性能对比 (原始测试集)")
    print("=" * 70)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 原始模型
    print("\n[1] 原始 TextCNN (原始数据训练)")
    acc1, n1 = evaluate_model(
        "data/models/router/best_model.pth",
        "data/processed/test_data.json",
        device
    )
    print(f"  测试准确率: {acc1*100:.2f}%")

    # 清洗后千问模型
    print("\n[2] TextCNN (清洗后千问数据训练)")
    acc2, n2 = evaluate_model(
        "data/models/router_cleaned/best_model.pth",
        "data/processed/test_data.json",
        device
    )
    print(f"  测试准确率: {acc2*100:.2f}%")

    print("\n" + "=" * 70)
    print("总结")
    print("=" * 70)
    print(f"原始 TextCNN (原始数据):     {acc1*100:.2f}%")
    print(f"TextCNN (清洗后千问数据):    {acc2*100:.2f}%")
    print(f"\n提升: {(acc2-acc1)*100:+.2f}%")


if __name__ == "__main__":
    main()
