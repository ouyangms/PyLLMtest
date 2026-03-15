"""
合并原始数据和增强数据
重新划分训练集/验证集/测试集
"""

import json
from pathlib import Path
from collections import Counter
import random
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router.category_config import CategoryConfig


def load_data():
    """加载原始数据"""
    data_dir = Path("data/processed")

    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open(data_dir / "val_data.json", "r", encoding="utf-8") as f:
        val_data = json.load(f)

    with open(data_dir / "test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    return train_data, val_data, test_data


def load_augmented_data(augmented_file: str = "data/processed/augmented_samples.json"):
    """加载增强数据"""
    try:
        with open(augmented_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def balance_samples(original_data: list, augmented_data: list, target_per_class: int = 500) -> list:
    """
    平衡每个类别的样本数

    Args:
        original_data: 原始数据
        augmented_data: 增强数据
        target_per_class: 每个类别目标样本数

    Returns:
        平衡后的数据
    """
    # 按类别分组
    original_by_class = {}
    augmented_by_class = {}

    for item in original_data:
        cat = item["category_id"]
        if cat not in original_by_class:
            original_by_class[cat] = []
        original_by_class[cat].append(item)

    for item in augmented_data:
        cat = item["category_id"]
        if cat not in augmented_by_class:
            augmented_by_class[cat] = []
        augmented_by_class[cat].append(item)

    # 合并并平衡
    balanced_data = []

    for cat_id in range(len(CategoryConfig.CATEGORIES)):
        cat_name = CategoryConfig.get_category_name(cat_id)

        original_count = len(original_by_class.get(cat_id, []))
        augmented_count = len(augmented_by_class.get(cat_id, []))

        print(f"{cat_name}: 原始={original_count}, 增强={augmented_count}", end="")

        # 原始样本不足，补充增强样本
        if original_count < target_per_class:
            needed = target_per_class - original_count
            available = augmented_count

            # 添加所有原始样本
            balanced_data.extend(original_by_class.get(cat_id, []))

            # 添加增强样本（如果可用）
            if available > 0:
                # 随机采样
                sample_count = min(needed, available)
                samples = random.sample(augmented_by_class[cat_id], sample_count)
                balanced_data.extend(samples)

                final_count = original_count + sample_count
                print(f" -> 补充{sample_count}个 = {final_count}")
            else:
                print(f" -> 无增强数据 = {original_count}")
        else:
            # 原始样本已足够
            balanced_data.extend(original_by_class.get(cat_id, []))
            print(f" -> 无需补充 = {original_count}")

    return balanced_data


def split_data(data: list, train_ratio: float = 0.7, val_ratio: float = 0.15, seed: int = 42) -> tuple:
    """
    划分数据集

    Args:
        data: 数据列表
        train_ratio: 训练集比例
        val_ratio: 验证集比例
        seed: 随机种子

    Returns:
        (train_data, val_data, test_data)
    """
    random.seed(seed)

    # 按类别分组（确保每个类别在各个集中都有样本）
    data_by_class = {}
    for item in data:
        cat = item["category_id"]
        if cat not in data_by_class:
            data_by_class[cat] = []
        data_by_class[cat].append(item)

    train_data = []
    val_data = []
    test_data = []

    for cat_id, items in data_by_class.items():
        # 打乱顺序
        random.shuffle(items)

        # 计算划分点
        n = len(items)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))

        train_data.extend(items[:train_end])
        val_data.extend(items[train_end:val_end])
        test_data.extend(items[val_end:])

    return train_data, val_data, test_data


def analyze_distribution(data: list, name: str = "数据集"):
    """分析数据分布"""
    print(f"\n{name}分布:")
    counter = Counter([item["category_id"] for item in data])

    for cat_id in range(len(CategoryConfig.CATEGORIES)):
        cat_name = CategoryConfig.get_category_name(cat_id)
        count = counter.get(cat_id, 0)
        print(f"  {cat_name}: {count}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="合并增强数据")
    parser.add_argument(
        "--augmented-file",
        type=str,
        default="data/processed/augmented_samples.json",
        help="增强数据文件"
    )
    parser.add_argument(
        "--target-per-class",
        type=int,
        default=500,
        help="每个类别目标样本数"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/processed",
        help="输出目录"
    )
    parser.add_argument(
        "--suffix",
        type=str,
        default="_augmented",
        help="输出文件后缀"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("合并增强数据")
    print("=" * 60)

    # 加载原始数据
    print("\n加载原始数据...")
    train_data, val_data, test_data = load_data()
    original_data = train_data + val_data + test_data
    print(f"原始数据总数: {len(original_data)}")

    # 加载增强数据
    print(f"\n加载增强数据: {args.augmented_file}")
    augmented_data = load_augmented_data(args.augmented_file)
    print(f"增强数据总数: {len(augmented_data)}")

    if not augmented_data:
        print("[警告] 未找到增强数据，仅使用原始数据")

    # 合并并平衡
    print(f"\n平衡数据（目标每类 {args.target_per_class} 样本）...")
    balanced_data = balance_samples(original_data, augmented_data, args.target_per_class)
    print(f"\n平衡后总数: {len(balanced_data)}")

    # 重新划分
    print("\n重新划分数据集...")
    new_train, new_val, new_test = split_data(balanced_data)

    print(f"\n划分结果:")
    print(f"  训练集: {len(new_train)}")
    print(f"  验证集: {len(new_val)}")
    print(f"  测试集: {len(new_test)}")

    # 分析分布
    analyze_distribution(new_train, "训练集")
    analyze_distribution(new_val, "验证集")
    analyze_distribution(new_test, "测试集")

    # 保存
    output_dir = Path(args.output_dir)
    suffix = args.suffix

    with open(output_dir / f"train_data{suffix}.json", "w", encoding="utf-8") as f:
        json.dump(new_train, f, ensure_ascii=False, indent=2)

    with open(output_dir / f"val_data{suffix}.json", "w", encoding="utf-8") as f:
        json.dump(new_val, f, ensure_ascii=False, indent=2)

    with open(output_dir / f"test_data{suffix}.json", "w", encoding="utf-8") as f:
        json.dump(new_test, f, ensure_ascii=False, indent=2)

    print(f"\n已保存到: {output_dir}")
    print(f"  - train_data{suffix}.json")
    print(f"  - val_data{suffix}.json")
    print(f"  - test_data{suffix}.json")


if __name__ == "__main__":
    main()
