"""
对比所有模型在原始测试集上的表现
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig


def evaluate_model(model_path, test_data, vocab, device="cuda"):
    """评估模型"""
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
    return accuracy


def main():
    # 加载测试数据
    with open("data/processed/test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    print(f"测试样本数: {len(test_data)}")

    vocab = CategoryConfig.create_vocabulary()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 定义模型
    models = {
        "原始 TextCNN (原始数据)": "data/models/router/best_model.pth",
        "TextCNN (清洗数据)": "data/models/router_clean/best_model.pth",
        "TextCNN (千问清洗数据)": "data/models/router_cleaned/best_model.pth",
        "TextCNN (Focal Loss)": "data/models/router_focal/best_model.pth",
    }

    print("\n" + "=" * 70)
    print("所有模型对比 (原始测试集)")
    print("=" * 70)

    results = {}
    for name, path in models.items():
        try:
            acc = evaluate_model(path, test_data, vocab, device)
            results[name] = acc
            print(f"\n{name:<35s}: {acc*100:.2f}%")
        except Exception as e:
            print(f"\n{name:<35s}: 错误 - {e}")

    # 排序
    print("\n" + "=" * 70)
    print("排名")
    print("=" * 70)
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for i, (name, acc) in enumerate(sorted_results, 1):
        diff = acc - sorted_results[0][1]
        print(f"{i}. {name:<35s}: {acc*100:.2f}%")


if __name__ == "__main__":
    main()
