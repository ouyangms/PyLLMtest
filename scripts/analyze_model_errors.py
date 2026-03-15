"""
分析模型错误，对比不同模型在各类别上的表现
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig


def evaluate_model_detailed(model_path, test_data, vocab, device="cuda"):
    """评估模型并返回详细结果"""
    model = TextCNNLite(len(vocab), num_classes=13)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    # 按类别统计
    by_category_correct = defaultdict(int)
    by_category_total = defaultdict(int)
    confusion = defaultdict(lambda: defaultdict(int))

    batch_size = 128

    with torch.no_grad():
        for i in range(0, len(test_data), batch_size):
            batch_end = min(i + batch_size, len(test_data))
            batch_data = test_data[i:batch_end]

            indices_list = []
            labels = []
            categories = []

            for item in batch_data:
                indices = []
                for char in item["text"][:64]:
                    idx = vocab.get(char, vocab.get("<UNK>", 1))
                    indices.append(idx)

                if len(indices) < 64:
                    indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

                indices_list.append(indices)
                labels.append(item["category_id"])
                categories.append(item.get("category_name", item.get("category", "")))

            indices_tensor = torch.tensor(indices_list, dtype=torch.long).to(device)
            labels_tensor = torch.tensor(labels, dtype=torch.long).to(device)

            outputs = model(indices_tensor)
            _, predicted = torch.max(outputs, 1)

            # 统计
            for true_label, pred_label, category in zip(labels, predicted.tolist(), categories):
                by_category_total[category] += 1
                if true_label == pred_label:
                    by_category_correct[category] += 1

                # 混淆矩阵（按类别名称）
                true_cat = CategoryConfig.CATEGORIES[true_label]
                pred_cat = CategoryConfig.CATEGORIES[pred_label]
                confusion[true_cat][pred_cat] += 1

    # 计算各类别准确率
    category_accuracy = {}
    for cat in by_category_total:
        if by_category_total[cat] > 0:
            category_accuracy[cat] = by_category_correct[cat] / by_category_total[cat]

    return category_accuracy, confusion, by_category_total


def main():
    print("=" * 80)
    print("模型错误分析")
    print("=" * 80)

    # 加载测试数据
    with open("data/processed/test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    print(f"\n测试样本数: {len(test_data)}")

    # 类别分布
    from collections import Counter
    dist = Counter([item.get("category_name", item.get("category", "")) for item in test_data])
    print("\n测试集类别分布:")
    for cat, count in sorted(dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:4d}")

    vocab = CategoryConfig.create_vocabulary()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 评估两个模型
    print("\n" + "=" * 80)
    print("[1] 评估原始模型")
    print("=" * 80)

    acc1, conf1, total1 = evaluate_model_detailed(
        "data/models/router/best_model.pth",
        test_data,
        vocab,
        device
    )

    print("\n各类别准确率:")
    for cat in sorted(acc1.keys(), key=lambda x: acc1[x]):
        print(f"  {cat:20s}: {acc1[cat]*100:5.2f}% (样本数: {total1[cat]})")

    print("\n" + "=" * 80)
    print("[2] 评估清洗后千问模型")
    print("=" * 80)

    acc2, conf2, total2 = evaluate_model_detailed(
        "data/models/router_cleaned/best_model.pth",
        test_data,
        vocab,
        device
    )

    print("\n各类别准确率:")
    for cat in sorted(acc2.keys(), key=lambda x: acc2[x]):
        print(f"  {cat:20s}: {acc2[cat]*100:5.2f}% (样本数: {total2[cat]})")

    # 对比
    print("\n" + "=" * 80)
    print("各类别准确率对比")
    print("=" * 80)
    print(f"{'类别':<20} {'原始模型':>10} {'千问模型':>10} {'差异':>10}")
    print("-" * 52)

    for cat in sorted(total1.keys()):
        orig_acc = acc1.get(cat, 0)
        qwen_acc = acc2.get(cat, 0)
        diff = qwen_acc - orig_acc
        print(f"{cat:<20} {orig_acc*100:>9.2f}% {qwen_acc*100:>9.2f}% {diff*100:>+9.2f}%")


if __name__ == "__main__":
    main()
