"""
深入分析原始模型的错误，找出准确率瓶颈
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig


def analyze_predictions(model, test_data, vocab, device="cuda"):
    """分析预测结果"""
    model.load_state_dict(torch.load("data/models/router/best_model.pth", map_location=device))
    model.to(device)
    model.eval()

    errors = []  # 错误样本
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
            texts = []

            for item in batch_data:
                indices = []
                text = item["text"]
                texts.append(text)

                for char in text[:64]:
                    idx = vocab.get(char, vocab.get("<UNK>", 1))
                    indices.append(idx)

                if len(indices) < 64:
                    indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

                indices_list.append(indices)
                labels.append(item["category_id"])

            indices_tensor = torch.tensor(indices_list, dtype=torch.long).to(device)
            labels_tensor = torch.tensor(labels, dtype=torch.long).to(device)

            outputs = model(indices_tensor)
            _, predicted = torch.max(outputs, 1)

            for text, true_label, pred_label in zip(texts, labels, predicted.tolist()):
                true_cat = CategoryConfig.CATEGORIES[true_label]
                pred_cat = CategoryConfig.CATEGORIES[pred_label]

                by_category_total[true_cat] += 1
                confusion[true_cat][pred_cat] += 1

                if true_label == pred_label:
                    by_category_correct[true_cat] += 1
                else:
                    errors.append({
                        "text": text,
                        "true": true_cat,
                        "pred": pred_cat,
                        "true_id": true_label,
                        "pred_id": pred_label
                    })

    return by_category_correct, by_category_total, confusion, errors


def main():
    print("=" * 80)
    print("深入分析原始模型的错误")
    print("=" * 80)

    # 加载测试数据
    with open("data/processed/test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    print(f"\n测试样本数: {len(test_data)}")

    vocab = CategoryConfig.create_vocabulary()
    model = TextCNNLite(len(vocab), num_classes=13)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 分析预测
    correct, total, confusion, errors = analyze_predictions(model, test_data, vocab, device)

    # 各类别准确率
    print("\n" + "=" * 80)
    print("各类别准确率 (从低到高)")
    print("=" * 80)

    category_acc = {}
    for cat in sorted(total.keys(), key=lambda x: correct[x]/total[x] if total[x] > 0 else 0):
        acc = correct[cat] / total[cat] if total[cat] > 0 else 0
        category_acc[cat] = acc
        print(f"{cat:20s}: {acc*100:5.2f}%  ({correct[cat]:3d}/{total[cat]:3d})")

    # 错误样本分析
    print("\n" + "=" * 80)
    print("错误样本分析")
    print("=" * 80)
    print(f"总错误数: {len(errors)}")

    # 按真实类别分组错误
    errors_by_true = defaultdict(list)
    for err in errors:
        errors_by_true[err["true"]].append(err)

    print("\n各类别错误数:")
    for cat in sorted(errors_by_true.keys(), key=lambda x: len(errors_by_true[x]), reverse=True):
        err_count = len(errors_by_true[cat])
        total_count = total[cat]
        print(f"  {cat:20s}: {err_count:3d} 个错误 (总样本: {total_count})")

    # 显示混淆严重的类别对
    print("\n" + "=" * 80)
    print("混淆矩阵 (Top 10)")
    print("=" * 80)

    conf_pairs = []
    for true_cat, preds in confusion.items():
        for pred_cat, count in preds.items():
            if true_cat != pred_cat and count > 0:
                conf_pairs.append((true_cat, pred_cat, count))

    conf_pairs.sort(key=lambda x: x[2], reverse=True)

    for true_cat, pred_cat, count in conf_pairs[:10]:
        print(f"  {true_cat:20s} -> {pred_cat:20s}: {count:3d}")

    # 具体错误示例
    print("\n" + "=" * 80)
    print("典型错误示例")
    print("=" * 80)

    # 按混淆对显示示例
    shown_pairs = set()
    for err in errors:
        pair = (err["true"], err["pred"])
        if pair not in shown_pairs and len(shown_pairs) < 15:
            print(f"\n{err['true']} -> {err['pred']}:")
            print(f"  文本: \"{err['text']}\"")
            shown_pairs.add(pair)

    # 分析问题样本
    print("\n" + "=" * 80)
    print("问题样本分析")
    print("=" * 80)

    # 极短样本
    very_short = [e for e in errors if len(e["text"]) <= 2]
    print(f"\n极短错误样本 (<=2字): {len(very_short)}")
    if very_short:
        print("示例:", [e["text"] for e in very_short[:5]])

    # 高频错误文本
    error_texts = [e["text"] for e in errors]
    text_counts = Counter(error_texts)
    print(f"\n重复错误文本 (出现2次以上):")
    for text, count in text_counts.most_common(10):
        if count > 1:
            print(f"  \"{text}\": {count} 次")


if __name__ == "__main__":
    main()
