"""
评估混合模型在不同测试集上的表现
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
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)
        model.eval()
    except Exception as e:
        print(f"无法加载模型: {e}")
        return None

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
    data_dir = Path("data/processed")

    # 加载测试数据
    with open(data_dir / "test_data.json", "r", encoding="utf-8") as f:
        test_data_original = json.load(f)

    with open(data_dir / "test_data_clean.json", "r", encoding="utf-8") as f:
        test_data_clean = json.load(f)

    vocab = CategoryConfig.create_vocabulary()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("=" * 70)
    print("模型对比评估")
    print("=" * 70)

    # 定义所有模型
    models = {
        "原始模型": "data/models/router/best_model.pth",
        "清洗模型": "data/models/router_clean_final/best_model.pth",
        "混合模型": "data/models/router_hybrid/best_model.pth",
    }

    results = {}

    for model_name, model_path in models.items():
        print(f"\n评估: {model_name}")
        print(f"  路径: {model_path}")

        # 原始测试集
        acc_orig = evaluate_model(model_path, test_data_original, vocab, device)
        if acc_orig is not None:
            print(f"  原始测试集: {acc_orig*100:.2f}%")

        # 清洗后测试集
        acc_clean = evaluate_model(model_path, test_data_clean, vocab, device)
        if acc_clean is not None:
            print(f"  清洗测试集: {acc_clean*100:.2f}%")

        if acc_orig is not None and acc_clean is not None:
            results[model_name] = {
                "original": acc_orig,
                "clean": acc_clean,
                "gap": acc_clean - acc_orig
            }

    # 总结
    print("\n" + "=" * 70)
    print("总结")
    print("=" * 70)

    print(f"\n{'模型':<15} {'原始测试集':>15} {'清洗测试集':>15} {'差距':>15}")
    print("-" * 62)

    for model_name, res in results.items():
        print(f"{model_name:<15} {res['original']*100:>14.2f}% {res['clean']*100:>14.2f}% {res['gap']*100:>+14.2f}%")

    # 推荐
    print("\n推荐:")
    if "混合模型" in results:
        hybrid = results["混合模型"]
        if hybrid["original"] > 0.60:  # 在原始测试集上达到60%+
            print("  ✅ 混合模型适合处理真实用户输入（包含模糊样本）")
        if hybrid["clean"] > 0.95:
            print("  ✅ 混合模型在有效样本上表现优秀")


if __name__ == "__main__":
    main()
