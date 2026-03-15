"""
车控语音助手 - 完整集成演示
展示路由+检索+LLM的端到端系统
"""

import sys
import json
import time
from pathlib import Path
from typing import List

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.inference_engine import InferenceEngine
from src.hybrid.architecture import ArchitectureSpec, print_architecture_overview


class VehicleAssistantDemo:
    """车控语音助手演示"""

    def __init__(self):
        """初始化助手"""
        print("=" * 70)
        print("车控语音助手 - 端到端系统")
        print("=" * 70)

        # 显示架构
        print("\n系统架构:")
        print("-" * 70)
        print_architecture_overview()

        # 初始化推理引擎
        print("\n初始化推理引擎...")
        self.engine = InferenceEngine(
            router_model_path="data/models/router_clean_final/best_model.pth",
            skills_dir=None,  # 使用模拟技能
            use_llm=False,    # 暂时使用规则引擎
            device="cuda" if self._check_cuda() else "cpu"
        )

        # 显示统计信息
        stats = self.engine.get_stats()
        print(f"\n系统信息:")
        print(f"  技能总数: {stats['total_skills']}")
        print(f"  类别数: {len(stats['categories'])}")
        print(f"  设备: {stats['device']}")

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
            "latency_ms": result.latency_ms
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

                print(f"  [路径: {result['processing_path']}, 置信度: {result['confidence']:.2f}, 延迟: {result['latency_ms']:.2f}ms]")

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
        print(f"  配置:")
        for key, value in stats['config'].items():
            print(f"    {key}: {value}")

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
                "inputs": ["温度24度", "音量大点", "导航到天安门"]
            },
            {
                "name": "多轮对话",
                "inputs": ["调一调", "温度"]
            },
            {
                "name": "模糊输入",
                "inputs": ["弄一下", "高点"]
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
                print(f"  [路径: {result['processing_path']}, 置信度: {result['confidence']:.2f}]")

    def save_results(self, results: List[dict], output_path: str):
        """保存结果到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存: {output_path}")

    def benchmark(self, num_iterations: int = 100):
        """性能基准测试"""
        print("\n" + "=" * 70)
        print("性能基准测试")
        print("=" * 70)

        test_inputs = [
            "打开空调", "座椅加热", "播放音乐", "导航到公司",
            "关闭车窗", "调节音量", "打开座椅通风"
        ]

        latencies = []

        print(f"\n运行 {num_iterations} 次推理...")

        for i in range(num_iterations):
            user_input = test_inputs[i % len(test_inputs)]

            start = time.perf_counter()
            result = self.process_input(user_input, f"bench_{i}")
            latency = (time.perf_counter() - start) * 1000

            latencies.append(latency)

            if (i + 1) % 20 == 0:
                print(f"  完成 {i + 1}/{num_iterations}")

        # 计算统计数据
        import numpy as np
        latencies = np.array(latencies)

        print(f"\n性能统计:")
        print(f"  平均延迟: {np.mean(latencies):.2f} ms")
        print(f"  中位数: {np.median(latencies):.2f} ms")
        print(f"  P95: {np.percentile(latencies, 95):.2f} ms")
        print(f"  P99: {np.percentile(latencies, 99):.2f} ms")
        print(f"  最小值: {np.min(latencies):.2f} ms")
        print(f"  最大值: {np.max(latencies):.2f} ms")


def main():
    """主函数"""
    demo = VehicleAssistantDemo()

    # 运行交互模式
    demo.run_cli()


if __name__ == "__main__":
    main()
