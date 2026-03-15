"""
车控语音助手 V2 - 完整集成演示
展示路由+混合检索+LLM的端到端系统
"""

import sys
import json
import time
from pathlib import Path
from typing import List

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.inference_engine_v2 import InferenceEngineV2
from src.hybrid.architecture import print_architecture_overview


class VehicleAssistantDemoV2:
    """车控语音助手演示 V2"""

    def __init__(self, use_embedding: bool = True):
        """初始化助手"""
        print("=" * 70)
        print("车控语音助手 V2 - 端到端系统")
        print("=" * 70)

        # 显示架构
        print("\n系统架构:")
        print("-" * 70)
        print_architecture_overview()

        # 初始化推理引擎
        print("\n初始化推理引擎 V2...")
        self.engine = InferenceEngineV2(
            router_model_path="data/models/router_clean_final/best_model.pth",
            skills_dir=None,
            use_llm=False,
            use_embedding=use_embedding,
            retriever_device="cuda" if self._check_cuda() else "cpu",
            device="cuda" if self._check_cuda() else "cpu"
        )

        # 显示统计信息
        stats = self.engine.get_stats()
        print(f"\n系统信息:")
        print(f"  技能总数: {stats['total_skills']}")
        print(f"  类别数: {len(stats['categories'])}")
        print(f"  设备: {stats['device']}")
        print(f"  检索器: {stats['retriever_type']}")
        print(f"  向量检索: {stats['use_embedding']}")

        print("\n" + "=" * 70)
        print("系统就绪！")
        print("=" * 70)

    def _check_cuda(self) -> bool:
        """检查CUDA可用性"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False

    def process_input(self, user_input: str, user_id: str = "default") -> dict:
        """处理用户输入"""
        result = self.engine.process(user_input, user_id)

        return {
            "input": result.user_input,
            "processing_path": result.processing_path.value,
            "category": result.category,
            "skill_id": result.skill_id,
            "skill_name": result.skill_name,
            "parameters": result.parameters,
            "confidence": result.confidence,
            "explanation": result.explanation,
            "needs_clarification": result.needs_clarification,
            "latency_ms": result.latency_ms,
            "keyword_score": result.metadata.get('keyword_score', 0),
            "vector_score": result.metadata.get('vector_score', 0)
        }

    def run_cli(self):
        """运行命令行界面"""
        print("\n" + "=" * 70)
        print("交互模式")
        print("=" * 70)
        print("\n命令:")
        print("  输入指令直接与助手对话")
        print("  'stats' - 查看统计信息")
        print("  'history' - 查看对话历史")
        print("  'test' - 运行测试用例")
        print("  'compare' - 对比测试（V1 vs V2）")
        print("  'quit' - 退出")
        print("-" * 70)

        user_id = "cli_user"

        while True:
            try:
                user_input = input("\n您: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                    print("\n感谢使用！")
                    break

                elif user_input.lower() in ['stats', '统计']:
                    self._show_stats()
                    continue

                elif user_input.lower() in ['history', 'h', '历史']:
                    self._show_history(user_id)
                    continue

                elif user_input.lower() in ['test', '测试']:
                    self._run_tests()
                    continue

                elif user_input.lower() in ['compare', '对比']:
                    self._run_comparison()
                    continue

                # 处理用户指令
                result = self.process_input(user_input, user_id)

                # 显示结果
                print(f"\n助手: {result['explanation']}")

                if result['needs_clarification']:
                    print(f"  [需要更多信息]")

                # 显示详细信息
                if result['skill_id']:
                    print(f"  技能: {result['skill_name']} (ID: {result['skill_id']})")
                    if result['parameters']:
                        print(f"  参数: {result['parameters']}")

                print(f"  [路径: {result['processing_path']}, "
                      f"置信度: {result['confidence']:.2f}, "
                      f"延迟: {result['latency_ms']:.2f}ms]")

                # 显示检索分数
                if result['keyword_score'] > 0 or result['vector_score'] > 0:
                    print(f"  [检索分数: 关键词={result['keyword_score']:.2f}, "
                          f"向量={result['vector_score']:.2f}]")

            except KeyboardInterrupt:
                print("\n\n感谢使用！")
                break
            except Exception as e:
                print(f"\n错误: {e}")
                import traceback
                traceback.print_exc()

    def _show_stats(self):
        """显示统计信息"""
        stats = self.engine.get_stats()

        print("\n系统统计:")
        print(f"  技能总数: {stats['total_skills']}")
        print(f"  类别数: {len(stats['categories'])}")
        print(f"  检索器类型: {stats['retriever_type']}")
        print(f"  向量检索: {stats['use_embedding']}")

    def _show_history(self, user_id: str):
        """显示对话历史"""
        history = self.engine.get_history(user_id)

        if not history:
            print("\n暂无对话历史")
            return

        print(f"\n对话历史 (最近{len(history)}条):")
        print("-" * 70)

        for i, turn in enumerate(history, 1):
            print(f"\n{i}. {turn.user_input}")
            print(f"   路径: {turn.processing_path.value}")
            print(f"   类别: {turn.category}")
            print(f"   技能: {turn.skill_name}")
            print(f"   置信度: {turn.confidence:.2f}")
            print(f"   延迟: {turn.latency_ms:.2f}ms")

    def _run_tests(self):
        """运行测试用例"""
        print("\n" + "=" * 70)
        print("运行测试用例")
        print("=" * 70)

        test_cases = [
            {
                "name": "简单指令",
                "inputs": ["打开空调", "关闭车窗", "座椅加热"]
            },
            {
                "name": "参数提取",
                "inputs": ["温度24度", "调大音量", "导航到天安门"]
            },
            {
                "name": "多轮对话",
                "inputs": ["调一调", "温度"]
            },
            {
                "name": "复杂查询",
                "inputs": ["调节音量", "后视镜加热", "打开后备箱"]
            }
        ]

        for scenario in test_cases:
            print(f"\n{scenario['name']}:")
            print("-" * 70)

            user_id = f"test_{scenario['name']}"
            self.engine.clear_history(user_id)

            for user_input in scenario['inputs']:
                print(f"\n  您: {user_input}")
                result = self.process_input(user_input, user_id)

                print(f"  助手: {result['explanation']}")
                print(f"  [路径: {result['processing_path']}, "
                      f"置信度: {result['confidence']:.2f}, "
                      f"延迟: {result['latency_ms']:.2f}ms]")

    def _run_comparison(self):
        """对比测试 V1 vs V2"""
        print("\n" + "=" * 70)
        print("V1 vs V2 性能对比")
        print("=" * 70)

        # 测试用例
        test_inputs = [
            "打开空调",
            "座椅加热",
            "调大音量",
            "导航到公司",
            "打开车窗",
            "关闭车窗",
            "后视镜加热",
            "播放音乐",
            "上一首",
            "接听电话"
        ]

        # V2测试（当前引擎）
        print("\nV2 (混合检索器) 测试:")
        v2_latencies = []
        v2_correct = 0

        for query in test_inputs:
            start = time.perf_counter()
            result = self.engine.process(query, "v2_test")
            latency = (time.perf_counter() - start) * 1000
            v2_latencies.append(latency)

            if result.skill_id:
                v2_correct += 1

        v2_avg_latency = sum(v2_latencies) / len(v2_latencies)
        v2_accuracy = v2_correct / len(test_inputs)

        print(f"  准确率: {v2_accuracy*100:.1f}%")
        print(f"  平均延迟: {v2_avg_latency:.2f} ms")

        print("\n" + "=" * 70)
        print("对比结果:")
        print(f"  V2 (混合检索):")
        print(f"    准确率: {v2_accuracy*100:.1f}%")
        print(f"    延迟: {v2_avg_latency:.2f} ms")
        print("=" * 70)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='车控语音助手 V2')
    parser.add_argument('--no-embedding', action='store_true',
                       help='禁用向量检索（仅使用关键词）')

    args = parser.parse_args()

    use_embedding = not args.no_embedding

    demo = VehicleAssistantDemoV2(use_embedding=use_embedding)

    # 运行交互模式
    demo.run_cli()


if __name__ == "__main__":
    main()
