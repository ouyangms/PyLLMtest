"""
服务模式 - 引擎长期运行，通过管道接收指令
避免每次都重新加载引擎
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.hybrid.inference_engine_v3 import InferenceEngineV3


def main():
    print("=" * 70)
    print("服务模式 - 引擎长期运行")
    print("=" * 70)

    # 只加载一次引擎
    print("\n[初始化引擎...]")
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
    print("\n[OK] 引擎已就绪，等待指令...\n")

    # 从标准输入读取指令
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            query = line.strip()
            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q']:
                print("\n[退出服务模式]")
                break

            # 处理指令
            result = engine.process(query, "service_user")

            # 输出结果（简化格式）
            output = {
                "input": query,
                "category": result.category,
                "skill": result.skill_name,
                "confidence": result.confidence,
                "latency_ms": result.latency_ms,
                "success": not result.needs_clarification,
                "message": result.explanation
            }

            # 输出JSON
            import json
            print(json.dumps(output, ensure_ascii=False))
            sys.stdout.flush()

        except KeyboardInterrupt:
            print("\n\n[退出服务模式]")
            break
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
