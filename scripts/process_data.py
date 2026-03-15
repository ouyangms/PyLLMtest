"""
处理数据脚本
运行: python scripts/process_data.py
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.data_processor import DataProcessor
from src.router.category_config import classify_skills


def main():
    print("=" * 60)
    print("处理训练数据")
    print("=" * 60)

    # 创建处理器
    processor = DataProcessor()

    # 加载数据
    skills = processor.load_skills()

    if not skills:
        print("错误: 没有加载到技能数据")
        print("提示: 先运行 python scripts/parse_skills.py 和 python scripts/generate_queries.py")
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

    # 生成路由数据
    print("\n生成路由分类器数据...")
    router_data = processor.generate_router_data(augment=True)
    train_data, val_data, test_data = processor.split_data(router_data, stratify=True)

    print(f"  训练集: {len(train_data)} 条")
    print(f"  验证集: {len(val_data)} 条")
    print(f"  测试集: {len(test_data)} 条")

    processor.save_router_data(train_data, val_data, test_data)

    # 生成检索数据
    print("\n生成向量检索数据...")
    retrieval_data = processor.generate_retrieval_data(augment=True)

    print("\n各分类数据量:")
    for cat, items in sorted(retrieval_data.items()):
        print(f"  {cat}: {len(items)} 条")

    processor.save_retrieval_data(retrieval_data)

    print("\n" + "=" * 60)
    print("数据处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
