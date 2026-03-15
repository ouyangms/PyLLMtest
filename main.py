"""
车控技能推理引擎 - 主入口

使用示例:
    python main.py parse                    # 解析技能
    python main.py generate                 # 生成训练样本
    python main.py train                    # 训练模型
    python main.py test "打开空调"           # 测试推理
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.router.classifier import RouterClassifier
from src.retrieval.vector_store import VectorStore
from src.data.skill_parser import SkillParser
from src.router.category_config import CategoryConfig


def parse_skills():
    """解析技能文件"""
    print("解析技能文件...")
    from scripts.parse_skills import main as parse_main
    parse_main()


def generate_queries():
    """生成训练样本"""
    print("生成训练样本...")
    from scripts.generate_queries import main as generate_main
    generate_main()


def process_data():
    """处理数据"""
    print("处理数据...")
    from scripts.process_data import main as process_main
    process_main()


def train_router():
    """训练路由模型"""
    print("训练路由模型...")
    from scripts.train_router import main as train_main
    train_main()


def build_indexes():
    """构建向量索引"""
    print("构建向量索引...")
    from scripts.build_indexes import main as build_main
    build_main()


def test_inference(query: str):
    """测试推理"""
    print("=" * 60)
    print("车控技能推理测试")
    print("=" * 60)
    print(f"用户指令: {query}")

    # 1. 路由分类
    print("\n[1/2] 路由分类...")
    try:
        classifier = RouterClassifier()
        category, probs = classifier.predict(query, return_probs=True)
        print(f"  预测分类: {category}")

        # 显示 Top-3
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        print(f"  Top-3 置信度:")
        for cat, prob in sorted_probs[:3]:
            print(f"    {cat}: {prob:.4f}")
    except Exception as e:
        print(f"  错误: {e}")
        print("  提示: 请先运行 python main.py train")
        category = None

    # 2. 向量检索
    print("\n[2/2] 向量检索...")
    try:
        store = VectorStore()
        results = store.search(query, category=category, k=3)

        print(f"  检索到 {len(results)} 条结果")
        for i, item in enumerate(results[:3], 1):
            print(f"\n  [{i}] 技能: {item.get('skill_name', 'N/A')}")
            print(f"      示例: {item.get('text', 'N/A')}")
            print(f"      分类: {item.get('category', 'N/A')}")
            print(f"      相似度: {item.get('score', 0):.4f}")
    except Exception as e:
        print(f"  错误: {e}")
        print("  提示: 请先运行 python main.py build")

    print("\n" + "=" * 60)


def interactive_mode():
    """交互模式"""
    print("=" * 60)
    print("车控技能推理引擎 - 交互模式")
    print("=" * 60)
    print("输入指令进行测试，输入 'quit' 退出")
    print("-" * 60)

    # 加载模型
    try:
        classifier = RouterClassifier()
        store = VectorStore()
        print("\n✓ 模型加载完成")
    except Exception as e:
        print(f"\n✗ 模型加载失败: {e}")
        print("提示: 请先运行训练和构建索引")
        return

    while True:
        try:
            query = input("\n用户指令: ").strip()

            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q', '退出']:
                print("再见!")
                break

            # 推理
            category = classifier.predict(query)
            results = store.search(query, category=category, k=3)

            print(f"\n路由: {category}")
            print(f"召回: {len(results)} 条")

            if results:
                print("\n候选技能:")
                for i, item in enumerate(results[:3], 1):
                    print(f"  {i}. {item.get('skill_name', 'N/A')}")

        except KeyboardInterrupt:
            print("\n\n再见!")
            break
        except Exception as e:
            print(f"错误: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="车控技能推理引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py parse                    解析技能文件
  python main.py generate                 生成训练样本
  python main.py process                  处理数据
  python main.py train                    训练模型
  python main.py build                    构建索引
  python main.py test "打开空调"           测试推理
  python main.py interactive              交互模式
        """
    )

    parser.add_argument(
        "command",
        choices=["parse", "generate", "process", "train", "build", "test", "interactive"],
        help="命令"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="测试指令"
    )

    args = parser.parse_args()

    if args.command == "parse":
        parse_skills()
    elif args.command == "generate":
        generate_queries()
    elif args.command == "process":
        process_data()
    elif args.command == "train":
        train_router()
    elif args.command == "build":
        build_indexes()
    elif args.command == "test":
        if not args.query:
            print("错误: 请提供测试指令")
            print("示例: python main.py test \"打开空调\"")
            return
        test_inference(args.query)
    elif args.command == "interactive":
        interactive_mode()


if __name__ == "__main__":
    main()
