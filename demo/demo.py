"""
多轮对话演示脚本
展示上下文感知对话功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 直接导入模块
from src.router.contextual_dialog import ContextualDialogRouter


class VehicleControlAssistant:
    """车控语音助手（简化版）"""
    def __init__(self):
        """初始化助手"""
        print("初始化车控语音助手...")

        model_path = "data/models/router_clean_final/best_model.pth"
        device = "cuda" if self._check_cuda() else "cpu"

        self.router = ContextualDialogRouter(
            model_path=model_path,
            device=device,
            history_len=5
        )

        self.current_user = "demo_user"

        print(f"[OK] 模型加载完成 ({device})")
        print(f"[OK] 助手就绪！")

    def _check_cuda(self) -> bool:
        """检查CUDA可用性"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False

    def process(self, user_input: str):
        """处理用户输入"""
        return self.router.process_input(user_input, self.current_user)

    def clear_history(self):
        """清除对话历史"""
        self.router.clear_history(self.current_user)


def demo_multi_turn():
    """演示多轮对话"""
    print("=" * 70)
    print("多轮对话演示")
    print("=" * 70)

    assistant = VehicleControlAssistant()

    # 演示场景
    scenarios = [
        {
            "name": "场景1: 分次表达意图",
            "description": "用户先说动作，后补充对象",
            "inputs": ["调一调", "温度"]
        },
        {
            "name": "场景2: 确认操作",
            "description": "系统提出建议，用户确认",
            "inputs": ["打开空调", "好的"]
        },
        {
            "name": "场景3: 逐步细化",
            "description": "用户逐步细化指令",
            "inputs": ["调节座椅", "左前", "加热"]
        },
        {
            "name": "场景4: 上下文理解",
            "description": "基于历史对话理解当前输入",
            "inputs": ["播放音乐", "声音大点"]
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'=' * 70}")
        print(f"{scenario['name']}")
        print(f"说明: {scenario['description']}")
        print(f"{'=' * 70}")

        # 清除历史
        assistant.clear_history()

        # 处理每轮对话
        for j, user_input in enumerate(scenario['inputs'], 1):
            print(f"\n[轮次 {j}]")
            print(f"用户: {user_input}")

            result = assistant.process(user_input)

            print(f"助手: {result['response']}")

            if result.get('used_context'):
                print(f"  [上下文组合] \"{result['original_input']}\" + 上下文 = \"{result['combined_input']}\"")

            print(f"  [识别结果] 类别: {result['category']}, 置信度: {result['confidence']:.2f}")

        print()


def demo_single_turn():
    """演示单次识别"""
    print("=" * 70)
    print("单次指令识别演示")
    print("=" * 70)

    assistant = VehicleControlAssistant()

    # 测试指令
    test_inputs = [
        "打开空调",
        "座椅加热",
        "导航到天安门",
        "播放音乐",
        "查询电量",
        "打开车窗",
        "关闭大灯",
    ]

    print("\n识别结果:")
    print("-" * 70)

    for user_input in test_inputs:
        result = assistant.process(user_input)

        status_mark = {
            "success": "[OK]",
            "low_confidence": "[?]",
            "clarification_needed": "[??]"
        }.get(result['status'], "[!]")

        print(f"{status_mark} {user_input:<20} → {result['category']:<20} ({result['confidence']:.2f})")


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("车控语音助手 - 功能演示")
    print("=" * 70)

    while True:
        print("\n请选择演示:")
        print("  1. 单次指令识别")
        print("  2. 多轮对话")
        print("  3. 全部演示")
        print("  0. 退出")

        choice = input("\n请输入选项: ").strip()

        if choice == "1":
            demo_single_turn()
        elif choice == "2":
            demo_multi_turn()
        elif choice == "3":
            demo_single_turn()
            demo_multi_turn()
        elif choice in ["0", "q", "exit", "退出"]:
            print("\n感谢使用！")
            break
        else:
            print("无效选项，请重新选择")


if __name__ == "__main__":
    main()
