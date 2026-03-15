"""
在清洗后的测试集上评估模型
对比原始模型和新模型
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
    # 加载数据
    data_dir = Path("data/processed")

    with open(data_dir / "test_data.json", "r", encoding="utf-8") as f:
        test_data_original = json.load(f)

    with open(data_dir / "test_data_clean.json", "r", encoding="utf-8") as f:
        test_data_clean = json.load(f)

    vocab = CategoryConfig.create_vocabulary()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("=" * 70)
    print("模型对比评估")
    print("=" * 70)

    print(f"\n原始测试集: {len(test_data_original)} 个样本")
    print(f"清洗后测试集: {len(test_data_clean)} 个样本")
    print(f"过滤无效样本: {len(test_data_original) - len(test_data_clean)} 个")

    # 原始模型
    print("\n" + "-" * 70)
    print("[原始模型] data/models/router/best_model.pth")
    print("-" * 70)

    acc_orig_orig = evaluate_model("data/models/router/best_model.pth", test_data_original, vocab, device)
    print(f"原始测试集准确率: {acc_orig_orig*100:.2f}%")

    acc_orig_clean = evaluate_model("data/models/router/best_model.pth", test_data_clean, vocab, device)
    print(f"清洗后测试集准确率: {acc_orig_clean*100:.2f}%")

    # 新模型
    print("\n" + "-" * 70)
    print("[新模型] data/models/router_clean_final/best_model.pth")
    print("-" * 70)

    acc_new_orig = evaluate_model("data/models/router_clean_final/best_model.pth", test_data_original, vocab, device)
    print(f"原始测试集准确率: {acc_new_orig*100:.2f}%")

    acc_new_clean = evaluate_model("data/models/router_clean_final/best_model.pth", test_data_clean, vocab, device)
    print(f"清洗后测试集准确率: {acc_new_clean*100:.2f}%")

    # 总结
    print("\n" + "=" * 70)
    print("总结")
    print("=" * 70)

    print(f"\n{'模型':<20} {'原始测试集':>15} {'清洗后测试集':>15}")
    print("-" * 52)
    print(f"{'原始模型':<20} {acc_orig_orig*100:>14.2f}% {acc_orig_clean*100:>14.2f}%")
    print(f"{'新模型':<20} {acc_new_orig*100:>14.2f}% {acc_new_clean*100:>14.2f}%")

    print("\n提升（清洗后测试集）:")
    print(f"  {(acc_new_clean - acc_orig_clean)*100:+.2f}%")

    print("\n验证:")
    print(f"  新模型在有效样本上达到 {acc_new_clean*100:.2f}% 准确率")
    print(f"  相比原始模型提升 {(acc_new_clean - acc_orig_clean)*100:+.2f}%")


if __name__ == "__main__":
    main()
