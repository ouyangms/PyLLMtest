"""
快速测试 - 引擎只加载一次，处理多个指令
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.hybrid.inference_engine_v3 import InferenceEngineV3


def main():
    print("=" * 70)
    print("快速测试 - 引擎加载一次，处理多个指令")
    print("=" * 70)

    # 只加载一次引擎
    print("\n[加载引擎...]")
    engine = InferenceEngineV3(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        use_embedding=True,
        retriever_device="cuda",
        device="cuda",
        execute_skills=True,
        use_mock_api=True
    )
    print("\n[OK] 引擎已加载，开始处理指令\n")

    # 测试指令
    queries = [
        "打开空调",
        "座椅加热",
        "调大音量",
        "导航到公司",
        "播放音乐",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] {query}")
        result = engine.process(query, "quick_test")

        # 简化输出
        status = "[OK]" if not result.needs_clarification else "[?]"
        exec_status = "[OK]" if result.execution_result and result.execution_result.status == 'success' else "[X]"

        print(f"  {status} 路由: {result.category or '未知'}")
        print(f"  路径: {result.processing_path.value}")

        if result.skill_id:
            print(f"  技能: {result.skill_name} (置信度: {result.confidence:.2f})")
            print(f"  执行: {exec_status} {result.execution_result.message if result.execution_result else '未执行'}")

        print(f"  延迟: {result.latency_ms:.2f}ms")

    print("\n" + "=" * 70)
    print("测试完成！注意：引擎只加载一次，后续指令处理很快")
    print("=" * 70)


if __name__ == "__main__":
    main()
