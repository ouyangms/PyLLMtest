"""
车控语音助手 - 交互式演示程序
支持单次预测、多轮对话、上下文理解
"""

import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router.contextual_dialog import ContextualDialogRouter


class VehicleControlAssistant:
    """车控语音助手"""

    def __init__(self):
        """初始化助手"""
        print("初始化车控语音助手...")

        # 使用清洗模型（在有效样本上表现优秀）
        model_path = "data/models/router_clean_final/best_model.pth"
        device = "cuda" if self._check_cuda() else "cpu"

        self.router = ContextualDialogRouter(
            model_path=model_path,
            device=device,
            history_len=5
        )

        self.current_user = "user"

        print(f"[OK] 模型加载完成 ({device})")
        print(f"[OK] 助手就绪！")

    def _check_cuda(self) -> bool:
        """检查CUDA可用性"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False

    def process(self, user_input: str) -> Dict:
        """处理用户输入"""
        result = self.router.process_input(user_input, self.current_user)
        return result

    def clear_history(self):
        """清除对话历史"""
        self.router.clear_history(self.current_user)
        print("对话历史已清除")

    def show_history(self):
        """显示对话历史"""
        history = self.router.get_history(self.current_user)
        if not history:
            print("暂无对话历史")
            return

        print(f"\n对话历史 (最近{len(history)}条):")
        print("-" * 70)
        for i, turn in enumerate(history, 1):
            print(f"{i}. 用户: {turn['user_input']}")
            if turn.get('used_context'):
                print(f"   (上下文: {turn['combined_input']})")
            print(f"   系统: {turn['system_response']}")
            print(f"   类别: {turn['predicted_category']}, 置信度: {turn['confidence']:.2f}")
            print()

    def show_categories(self):
        """显示支持的类别"""
        from src.router.category_config import CategoryConfig

        print("\n支持的指令类别:")
        print("-" * 70)
        for i, category in enumerate(CategoryConfig.CATEGORIES, 1):
            # 获取中文名称
            category_name_zh = {
                "climate_control": "空调控制",
                "seat_control": "座椅控制",
                "window_control": "车窗控制",
                "light_control": "灯光控制",
                "mirror_control": "后视镜控制",
                "door_control": "车门控制",
                "music_media": "音乐媒体",
                "navigation": "导航",
                "phone_call": "电话",
                "vehicle_info": "车辆信息",
                "system_settings": "系统设置",
                "driving_assist": "驾驶辅助",
                "charging_energy": "充电能源",
            }.get(category, category)

            print(f"  {i:2d}. {category_name_zh}")

    def show_examples(self):
        """显示示例指令"""
        print("\n示例指令:")
        print("-" * 70)
        examples = [
            "打开空调",
            "座椅加热",
            "导航到天安门",
            "播放音乐",
            "调节音量",
            "打开车窗",
            "关闭大灯",
            "查询电量",
            "多轮对话试试：\"调一调\" → \"温度\"",
        ]
        for example in examples:
            print(f"  - {example}")

    def run(self):
        """运行交互式界面"""
        print("\n" + "=" * 70)
        print("车控语音助手 - 交互式演示")
        print("=" * 70)

        self.show_examples()
        print("\n" + "-" * 70)
        print("命令:")
        print("  输入指令直接与助手对话")
        print("  'history' - 查看对话历史")
        print("  'categories' - 查看支持的类别")
        print("  'examples' - 查看更多示例")
        print("  'clear' - 清除对话历史")
        print("  'quit' 或 'exit' - 退出")
        print("-" * 70)

        while True:
            try:
                # 获取用户输入
                user_input = input("\n您: ").strip()

                if not user_input:
                    continue

                # 处理命令
                if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                    print("\n感谢使用！再见~")
                    break

                elif user_input.lower() in ['history', 'h', '历史']:
                    self.show_history()
                    continue

                elif user_input.lower() in ['categories', 'c', '类别']:
                    self.show_categories()
                    continue

                elif user_input.lower() in ['examples', 'e', '示例']:
                    self.show_examples()
                    continue

                elif user_input.lower() in ['clear', '清除']:
                    self.clear_history()
                    continue

                # 处理用户指令
                result = self.process(user_input)

                # 显示结果
                print(f"\n助手: {result['response']}")

                # 显示详细信息（调试用）
                if result.get('used_context'):
                    print(f"  [上下文] \"{result['original_input']}\" → \"{result['combined_input']}\"")

                # 低置信度提示
                if result['status'] == 'low_confidence':
                    print(f"  [置信度较低 {result['confidence']:.2f}] 请确认")

            except KeyboardInterrupt:
                print("\n\n感谢使用！再见~")
                break
            except Exception as e:
                print(f"\n错误: {e}")
                import traceback
                traceback.print_exc()


def main():
    """主函数"""
    assistant = VehicleControlAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
