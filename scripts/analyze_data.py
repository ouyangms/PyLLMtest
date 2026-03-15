"""
分析训练数据，识别准确率瓶颈
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router.category_config import CategoryConfig


def analyze_data_distribution():
    """分析数据分布"""
    print("=" * 60)
    print("数据分布分析")
    print("=" * 60)

    # 加载数据
    data_dir = Path("data/processed")

    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open(data_dir / "val_data.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    with open(data_dir / "test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # 统计每个类别的样本数
    def count_by_category(data):
        counter = Counter()
        for item in data:
            cat_id = item["category_id"]
            cat_name = CategoryConfig.get_category_name(cat_id)
            counter[cat_name] += 1
        return counter

    train_dist = count_by_category(train_data)
    val_dist = count_by_category(val_data)
    test_dist = count_by_category(test_data)

    print("\n类别分布:")
    print(f"{'类别':<25} {'训练集':<10} {'验证集':<10} {'测试集':<10} {'总计'}")
    print("-" * 70)

    for cat_name in sorted(CategoryConfig.CATEGORIES):
        train_count = train_dist.get(cat_name, 0)
        val_count = val_dist.get(cat_name, 0)
        test_count = test_dist.get(cat_name, 0)
        total = train_count + val_count + test_count
        print(f"{cat_name:<25} {train_count:<10} {val_count:<10} {test_count:<10} {total}")

    total_train = len(train_data)
    total_val = len(val_data)
    total_test = len(test_data)
    print("-" * 70)
    print(f"{'总计':<25} {total_train:<10} {total_val:<10} {total_test:<10} {total_train + total_val + total_test}")

    # 分析不平衡程度
    print("\n" + "=" * 60)
    print("类别不平衡分析")
    print("=" * 60)

    max_count = max(train_dist.values())
    min_count = min(train_dist.values())
    imbalance_ratio = max_count / min_count

    print(f"最大类别样本数: {max_count}")
    print(f"最小类别样本数: {min_count}")
    print(f"不平衡比例: {imbalance_ratio:.1f}:1")

    if imbalance_ratio > 5:
        print("[警告] 数据集存在严重类别不平衡！")
        print("建议: 使用类别权重或过采样/欠采样")

    # 分析文本长度分布
    print("\n" + "=" * 60)
    print("文本长度分析")
    print("=" * 60)

    all_lengths = [len(item["text"]) for item in train_data]
    avg_length = sum(all_lengths) / len(all_lengths)
    max_length = max(all_lengths)
    min_length = min(all_lengths)

    print(f"平均长度: {avg_length:.1f} 字符")
    print(f"最大长度: {max_length} 字符")
    print(f"最小长度: {min_length} 字符")

    # 长度分布
    length_50 = sum(1 for l in all_lengths if l <= 50)
    length_64 = sum(1 for l in all_lengths if l <= 64)
    length_100 = sum(1 for l in all_lengths if l <= 100)

    print(f"\n长度分布:")
    print(f"  <= 50 字符: {length_50 / len(all_lengths) * 100:.1f}%")
    print(f"  <= 64 字符: {length_64 / len(all_lengths) * 100:.1f}%")
    print(f"  <= 100 字符: {length_100 / len(all_lengths) * 100:.1f}%")

    # 分析重复样本
    print("\n" + "=" * 60)
    print("数据质量分析")
    print("=" * 60)

    train_texts = [item["text"] for item in train_data]
    text_counts = Counter(train_texts)
    duplicates = sum(1 for count in text_counts.values() if count > 1)
    duplicate_samples = sum(count - 1 for count in text_counts.values() if count > 1)

    print(f"唯一文本数: {len(text_counts)}")
    print(f"重复文本数: {duplicates}")
    print(f"重复样本数: {duplicate_samples}")
    print(f"重复率: {duplicate_samples / len(train_data) * 100:.1f}%")

    # 分析每个类别的查询示例
    print("\n" + "=" * 60)
    print("各类别示例查询")
    print("=" * 60)

    for cat_name in sorted(CategoryConfig.CATEGORIES):
        examples = [item["text"] for item in train_data if CategoryConfig.get_category_name(item["category_id"]) == cat_name]
        print(f"\n{cat_name} ({len(examples)} 样本):")
        for i, ex in enumerate(examples[:5]):
            print(f"  [{i+1}] {ex}")
        if len(examples) > 5:
            print(f"  ... 还有 {len(examples) - 5} 个样本")

    # 分析字符词汇表
    print("\n" + "=" * 60)
    print("字符词汇表分析")
    print("=" * 60)

    all_chars = []
    for item in train_data:
        all_chars.extend(list(item["text"]))

    char_counts = Counter(all_chars)
    vocab_size = len(char_counts)

    print(f"唯一字符数: {vocab_size}")
    print(f"总字符数: {len(all_chars)}")
    print(f"平均字符频率: {len(all_chars) / vocab_size:.1f}")

    # 罕见字符
    rare_chars = [char for char, count in char_counts.items() if count <= 5]
    print(f"罕见字符数 (出现<=5次): {len(rare_chars)}")

    # 分析每个类别的准确率瓶颈
    print("\n" + "=" * 60)
    print("潜在问题分析")
    print("=" * 60)

    # 类别不平衡
    imbalance_threshold = 0.05  # 5%
    total_samples = len(train_data)
    minority_classes = [cat for cat, count in train_dist.items() if count / total_samples < imbalance_threshold]
    if minority_classes:
        print(f"[问题1] 少数类别 (样本<{imbalance_threshold*100}%): {', '.join(minority_classes)}")
        print("  影响: 模型难以学习少数类别的特征")
        print("  建议: 增加这些类别的训练样本或使用类别权重")

    # 数据不足
    samples_per_class_threshold = 100
    insufficient_classes = [cat for cat, count in train_dist.items() if count < samples_per_class_threshold]
    if insufficient_classes:
        print(f"\n[问题2] 数据不足类别 (样本<{samples_per_class_threshold}): {', '.join(insufficient_classes)}")
        print("  影响: 模型容易过拟合")
        print("  建议: 使用 LLM 生成更多训练样本")

    # 高相似度类别
    print(f"\n[问题3] 类别间相似度分析")
    category_keywords = defaultdict(list)
    for item in train_data:
        cat_name = CategoryConfig.get_category_name(item["category_id"])
        category_keywords[cat_name].append(item["text"])

    # 找出可能混淆的类别对
    confusion_candidates = []
    categories = list(CategoryConfig.CATEGORIES)
    for i in range(len(categories)):
        for j in range(i + 1, len(categories)):
            cat1, cat2 = categories[i], categories[j]
            # 简单检查：是否有相同的关键词
            words1 = set(' '.join(category_keywords[cat1]).split())
            words2 = set(' '.join(category_keywords[cat2]).split())
            overlap = len(words1 & words2) / min(len(words1), len(words2)) if min(len(words1), len(words2)) > 0 else 0
            if overlap > 0.5:
                confusion_candidates.append((cat1, cat2, overlap))

    if confusion_candidates:
        print(f"  高相似度类别对 (可能混淆):")
        for cat1, cat2, overlap in sorted(confusion_candidates, key=lambda x: -x[2])[:5]:
            print(f"    {cat1} <-> {cat2}: 重叠度 {overlap:.1%}")

    return {
        "train_dist": train_dist,
        "val_dist": val_dist,
        "test_dist": test_dist,
        "imbalance_ratio": imbalance_ratio,
        "avg_length": avg_length,
        "duplicate_rate": duplicate_samples / len(train_data)
    }


if __name__ == "__main__":
    analyze_data_distribution()
