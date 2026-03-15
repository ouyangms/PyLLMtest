"""
数据处理器
生成路由分类器和向量检索的训练/测试数据
"""

import json
import random
from typing import Dict, List, Tuple, Any
from pathlib import Path
import numpy as np
from collections import defaultdict

from .skill_parser import SkillParser
from ..router.category_config import CategoryConfig, classify_skills


class DataProcessor:
    """数据处理器"""

    def __init__(self, skills: List[Dict] = None):
        """
        初始化数据处理器

        Args:
            skills: 技能列表
        """
        self.skills = skills or []
        self.vocab = CategoryConfig.create_vocabulary()

    def load_skills(self, skills_path: str = None) -> List[Dict]:
        """
        加载技能数据

        Args:
            skills_path: 技能数据库文件路径

        Returns:
            技能列表
        """
        if skills_path is None:
            skills_path = Path(__file__).parent.parent.parent / "data" / "processed" / "skills_with_queries.json"

        skills_path = Path(skills_path)

        if not skills_path.exists():
            # 尝试加载原始技能库
            alt_path = skills_path.parent / "skills_database.json"
            if alt_path.exists():
                skills_path = alt_path
            else:
                print(f"错误: 技能数据库不存在: {skills_path}")
                return []

        print(f"加载技能数据: {skills_path}")
        with open(skills_path, 'r', encoding='utf-8') as f:
            self.skills = json.load(f)

        print(f"加载了 {len(self.skills)} 个技能")
        return self.skills

    def augment_query(self, query: str, method: str = "synonym") -> str:
        """
        数据增强：对查询进行变换

        Args:
            query: 原始查询
            method: 增强方法 (synonym, omit, shuffle)

        Returns:
            增强后的查询
        """
        synonym_dict = CategoryConfig.get_synonym_dict()

        if method == "synonym":
            # 同义词替换
            for standard, synonyms in synonym_dict.items():
                for synonym in synonyms:
                    if synonym in query:
                        query = query.replace(synonym, standard)
                        return query

        elif method == "omit":
            # 省略主语
            if query.startswith("把") or query.startswith("将"):
                # "把主驾窗户打开" -> "窗户打开"
                parts = query.split("窗户")[1:] if "窗户" in query else []
                if parts:
                    return "窗户" + "".join(parts)

        elif method == "shuffle":
            # 句式变换（简单示例）
            if "的" in query:
                # "打开主驾的空调" -> "主驾空调打开"
                query = query.replace("的", "")

        return query

    def generate_router_data(
        self,
        augment: bool = True,
        augment_ratio: float = 0.3
    ) -> List[Dict]:
        """
        生成路由分类器的训练数据

        Args:
            augment: 是否进行数据增强
            augment_ratio: 数据增强比例

        Returns:
            训练数据列表，每项包含 {text, category_id, category_name}
        """
        data = []

        for skill in self.skills:
            category = skill.get("category", "system_settings")
            category_id = CategoryConfig.get_category_id(category)
            queries = skill.get("example_queries", [])

            # 添加原始查询
            for query in queries:
                if query.strip():
                    data.append({
                        "text": query.strip(),
                        "category_id": category_id,
                        "category_name": category,
                        "skill_id": skill.get("skill_id", ""),
                        "augmented": False
                    })

            # 数据增强
            if augment and queries:
                augment_count = int(len(queries) * augment_ratio)
                augment_indices = random.sample(range(len(queries)), min(augment_count, len(queries)))

                for idx in augment_indices:
                    original_query = queries[idx]
                    augmented_query = self.augment_query(original_query)

                    if augmented_query != original_query and augmented_query.strip():
                        data.append({
                            "text": augmented_query.strip(),
                            "category_id": category_id,
                            "category_name": category,
                            "skill_id": skill.get("skill_id", ""),
                            "augmented": True
                        })

        print(f"生成路由数据: {len(data)} 条")
        return data

    def generate_retrieval_data(
        self,
        augment: bool = True,
        augment_ratio: float = 0.2
    ) -> Dict[str, List[Dict]]:
        """
        生成向量检索的训练数据（按分类组织）

        Args:
            augment: 是否进行数据增强
            augment_ratio: 数据增强比例

        Returns:
            按分类组织的检索数据
        """
        data_by_category = defaultdict(list)

        for skill in self.skills:
            category = skill.get("category", "system_settings")
            queries = skill.get("example_queries", [])

            # 添加原始查询
            for query in queries:
                if query.strip():
                    data_by_category[category].append({
                        "text": query.strip(),
                        "skill_id": skill.get("skill_id", ""),
                        "skill_name": skill.get("name", ""),
                        "augmented": False
                    })

            # 数据增强
            if augment and queries:
                augment_count = int(len(queries) * augment_ratio)
                augment_indices = random.sample(range(len(queries)), min(augment_count, len(queries)))

                for idx in augment_indices:
                    original_query = queries[idx]
                    augmented_query = self.augment_query(original_query)

                    if augmented_query != original_query and augmented_query.strip():
                        data_by_category[category].append({
                            "text": augmented_query.strip(),
                            "skill_id": skill.get("skill_id", ""),
                            "skill_name": skill.get("name", ""),
                            "augmented": True
                        })

        # 转换为普通字典
        result = {cat: items for cat, items in data_by_category.items()}

        total = sum(len(items) for items in result.values())
        print(f"生成检索数据: {total} 条 (覆盖 {len(result)} 个分类)")

        return result

    def split_data(
        self,
        data: List[Dict],
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        stratify: bool = True
    ) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        划分训练集/验证集/测试集

        Args:
            data: 数据列表
            train_ratio: 训练集比例
            val_ratio: 验证集比例
            test_ratio: 测试集比例
            stratify: 是否按类别分层划分

        Returns:
            (train_data, val_data, test_data)
        """
        if not stratify:
            # 随机划分
            random.shuffle(data)
            n = len(data)
            train_end = int(n * train_ratio)
            val_end = train_end + int(n * val_ratio)

            return (
                data[:train_end],
                data[train_end:val_end],
                data[val_end:]
            )

        # 按类别分层划分
        data_by_category = defaultdict(list)
        for item in data:
            category = item.get("category_name", "system_settings")
            data_by_category[category].append(item)

        train_data, val_data, test_data = [], [], []

        for category, items in data_by_category.items():
            random.shuffle(items)
            n = len(items)
            train_end = int(n * train_ratio)
            val_end = train_end + int(n * val_ratio)

            train_data.extend(items[:train_end])
            val_data.extend(items[train_end:val_end])
            test_data.extend(items[val_end:])

        # 打乱
        random.shuffle(train_data)
        random.shuffle(val_data)
        random.shuffle(test_data)

        return train_data, val_data, test_data

    def save_router_data(
        self,
        train_data: List[Dict],
        val_data: List[Dict],
        test_data: List[Dict],
        output_dir: str = None
    ):
        """
        保存路由数据

        Args:
            train_data: 训练数据
            val_data: 验证数据
            test_data: 测试数据
            output_dir: 输出目录
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "data" / "processed"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir / "train_data.json", 'w', encoding='utf-8') as f:
            json.dump(train_data, f, ensure_ascii=False, indent=2)

        with open(output_dir / "val_data.json", 'w', encoding='utf-8') as f:
            json.dump(val_data, f, ensure_ascii=False, indent=2)

        with open(output_dir / "test_data.json", 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        print(f"已保存路由数据到: {output_dir}")

    def save_retrieval_data(
        self,
        retrieval_data: Dict[str, List[Dict]],
        output_dir: str = None
    ):
        """
        保存检索数据

        Args:
            retrieval_data: 检索数据字典
            output_dir: 输出目录
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "data" / "processed"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 保存合并数据
        all_data = []
        for category, items in retrieval_data.items():
            all_data.extend(items)

        with open(output_dir / "retrieval_data.json", 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        # 保存分类数据
        with open(output_dir / "retrieval_data_by_category.json", 'w', encoding='utf-8') as f:
            json.dump(retrieval_data, f, ensure_ascii=False, indent=2)

        print(f"已保存检索数据到: {output_dir}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取数据统计信息

        Returns:
            统计信息字典
        """
        stats = {
            "total_skills": len(self.skills),
            "total_queries": 0,
            "category_distribution": defaultdict(int),
        }

        for skill in self.skills:
            query_count = len(skill.get("example_queries", []))
            stats["total_queries"] += query_count
            category = skill.get("category", "unknown")
            stats["category_distribution"][category] += 1

        # 转换为普通字典
        stats["category_distribution"] = dict(stats["category_distribution"])

        return stats


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="数据处理器")
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/skills_with_queries.json",
        help="输入技能文件路径"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/processed",
        help="输出目录"
    )
    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.7,
        help="训练集比例"
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.15,
        help="验证集比例"
    )
    parser.add_argument(
        "--test-ratio",
        type=float,
        default=0.15,
        help="测试集比例"
    )
    parser.add_argument(
        "--augment",
        action="store_true",
        help="是否进行数据增强"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="随机种子"
    )

    args = parser.parse_args()

    # 设置随机种子
    random.seed(args.seed)
    np.random.seed(args.seed)

    print("=" * 60)
    print("数据处理开始")
    print("=" * 60)

    # 创建处理器
    processor = DataProcessor()

    # 加载数据
    skills = processor.load_skills(args.input)

    if not skills:
        print("错误: 没有加载到技能数据")
        return

    # 确保已分类
    skills = classify_skills(skills)
    processor.skills = skills

    # 打印统计
    print("\n数据统计:")
    stats = processor.get_statistics()
    print(f"  总技能数: {stats['total_skills']}")
    print(f"  总查询数: {stats['total_queries']}")
    print(f"  平均查询数: {stats['total_queries'] / stats['total_skills']:.2f}")

    print("\n分类分布:")
    for cat, count in sorted(stats["category_distribution"].items()):
        print(f"  {cat}: {count} 个技能")

    # 生成路由数据
    print("\n生成路由分类器数据...")
    router_data = processor.generate_router_data(augment=args.augment)
    train_data, val_data, test_data = processor.split_data(
        router_data,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        stratify=True
    )

    print(f"  训练集: {len(train_data)} 条")
    print(f"  验证集: {len(val_data)} 条")
    print(f"  测试集: {len(test_data)} 条")

    processor.save_router_data(train_data, val_data, test_data, args.output_dir)

    # 生成检索数据
    print("\n生成向量检索数据...")
    retrieval_data = processor.generate_retrieval_data(augment=args.augment)

    print("\n各分类数据量:")
    for cat, items in sorted(retrieval_data.items()):
        print(f"  {cat}: {len(items)} 条")

    processor.save_retrieval_data(retrieval_data, args.output_dir)

    print("\n" + "=" * 60)
    print("数据处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
