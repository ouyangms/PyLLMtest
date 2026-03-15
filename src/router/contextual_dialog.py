"""
上下文感知的多轮对话系统
结合历史对话理解用户意图
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import deque

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig


# 上下文模式
CONTEXT_PATTERNS = {
    # 补充对象
    "补充对象": ["温度", "风量", "座椅", "车窗", "音乐", "音量", "导航", "电话"],
    # 补充位置
    "补充位置": ["左前", "右前", "左后", "右后", "主驾", "副驾", "后排", "前", "后"],
    # 补充方向
    "补充方向": ["高点", "低点", "大点", "小点", "开大", "开小", "调高", "调低"],
    # 确认操作
    "确认操作": ["好的", "是的", "对", "确认", "行", "可以", "嗯"],
}


class ContextualDialogRouter:
    """上下文感知的对话路由器"""

    def __init__(self, model_path: str, device: str = "cuda", history_len: int = 5):
        """初始化"""
        self.vocab = CategoryConfig.create_vocabulary()
        self.device = device

        # 加载模型
        self.model = TextCNNLite(len(self.vocab), num_classes=13)
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.to(device)
        self.model.eval()

        # 对话历史（每个用户独立）
        self.user_histories: Dict[str, deque] = {}
        self.history_len = history_len

    def _get_user_history(self, user_id: str) -> deque:
        """获取用户历史"""
        if user_id not in self.user_histories:
            self.user_histories[user_id] = deque(maxlen=self.history_len)
        return self.user_histories[user_id]

    def _add_to_history(self, user_id: str, turn: Dict):
        """添加到历史"""
        history = self._get_user_history(user_id)
        history.append(turn)

    def _detect_context_type(self, text: str) -> Optional[str]:
        """检测输入的上下文类型"""
        for ctx_type, patterns in CONTEXT_PATTERNS.items():
            for pattern in patterns:
                if pattern in text:
                    return ctx_type
        return None

    def _classify_by_keywords(self, text: str) -> Optional[str]:
        """
        基于关键词的快速分类（规则回退）
        用于处理模型未学习到的特殊情况
        """
        # 空调控制关键词（最高优先级）
        climate_keywords = ["温度", "空调", "冷气", "暖气", "制冷", "制热", "除雾", "除霜", "ac", "hvac"]
        for keyword in climate_keywords:
            if keyword in text:
                return "climate_control"

        # 座椅控制
        if any(kw in text for kw in ["座椅", "座位", "坐垫"]):
            return "seat_control"

        # 音乐媒体
        if any(kw in text for kw in ["音乐", "音量", "播放", "暂停", "上一首", "下一首"]):
            return "music_media"

        # 导航
        if any(kw in text for kw in ["导航", "路线", "目的地"]):
            return "navigation"

        return None

    def _combine_with_context(self, text: str, history: deque) -> Tuple[str, bool]:
        """
        结合历史对话组合完整的意图
        返回: (组合后的文本, 是否使用了上下文)
        """
        if not history:
            return text, False

        last_turn = history[-1]
        last_input = last_turn.get("user_input", "")

        # 检测当前输入的类型
        context_type = self._detect_context_type(text)

        if context_type == "补充对象":
            # 例如："温度" → 前面是"调一调" → "调节温度"
            # 检查前一轮是否是动作
            for action in ["调", "调节", "设置", "打开", "关闭"]:
                if action in last_input:
                    return f"{action}{text}", True

            # 检查前一轮的预测类别
            if "predicted_category" in last_turn:
                category = last_turn["predicted_category"]
                # 根据类别生成完整表达
                if category == "climate_control":
                    return f"调节空调{text}", True
                elif category == "seat_control":
                    return f"调节座椅{text}", True
                elif category == "music_media":
                    return f"调节音乐{text}", True

        elif context_type == "补充位置":
            # 例如："左前" → 前面是"打开座椅加热" → "打开左前座椅加热"
            if "predicted_category" in last_turn:
                category = last_turn["predicted_category"]
                if category == "seat_control":
                    return f"{text}座椅加热", True
                elif category == "window_control":
                    return f"打开{last_input}", True

        elif context_type == "补充方向":
            # 例如："高点" → 前面是"调节空调" → "空调调高点"
            if "predicted_category" in last_turn:
                category = last_turn["predicted_category"]
                if category == "climate_control":
                    return f"空调{text}", True
                elif category == "music_media":
                    return f"音量{text}", True

        elif context_type == "确认操作":
            # 用户确认，使用前一轮的意图
            if "predicted_category" in last_turn:
                return last_input, True

        return text, False

    def predict_category(self, text: str) -> Tuple[str, float]:
        """预测类别"""
        # 编码文本
        indices = []
        for char in text[:64]:
            idx = self.vocab.get(char, self.vocab.get("<UNK>", 1))
            indices.append(idx)

        if len(indices) < 64:
            indices.extend([self.vocab.get("<PAD>", 0)] * (64 - len(indices)))

        indices_tensor = torch.tensor([indices], dtype=torch.long).to(self.device)

        # 预测
        with torch.no_grad():
            outputs = self.model(indices_tensor)
            probs = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)

            category_name = CategoryConfig.CATEGORIES[predicted.item()]

        return category_name, confidence.item()

    def process_input(
        self,
        text: str,
        user_id: str = "default"
    ) -> Dict:
        """
        处理用户输入（带上下文）
        """
        # 获取用户历史
        history = self._get_user_history(user_id)

        # 尝试结合上下文
        combined_text, used_context = self._combine_with_context(text, history)

        if used_context:
            print(f"[上下文] \"{text}\" + 上下文 → \"{combined_text}\"")

        # 预测
        category, confidence = self.predict_category(combined_text)

        # 关键词规则回退（当置信度低或检测到特定关键词时）
        rule_category = self._classify_by_keywords(text)
        if rule_category and (confidence < 0.8 or rule_category != category):
            print(f"[规则回退] \"{text}\" 模型分类: {category} (置信度: {confidence:.2f}) → 规则修正: {rule_category}")
            category = rule_category
            confidence = 0.85  # 规则匹配置信度

        # 构建响应
        if used_context and confidence > 0.5:
            response = f"好的，明白了，为您{combined_text}"
            status = "success"
        elif confidence > 0.7:
            response = f"好的，正在为您{combined_text}"
            status = "success"
        else:
            response = f"请问您是想{combined_text}吗？"
            status = "low_confidence"

        # 记录到历史
        self._add_to_history(user_id, {
            "user_input": text,
            "combined_input": combined_text,
            "used_context": used_context,
            "predicted_category": category,
            "confidence": confidence,
            "system_response": response
        })

        return {
            "status": status,
            "category": category,
            "confidence": confidence,
            "response": response,
            "used_context": used_context,
            "original_input": text,
            "combined_input": combined_text
        }

    def clear_history(self, user_id: str = "default"):
        """清除用户历史"""
        if user_id in self.user_histories:
            self.user_histories[user_id].clear()

    def get_history(self, user_id: str = "default") -> List[Dict]:
        """获取用户历史"""
        return list(self._get_user_history(user_id))


def demo_contextual_dialog():
    """演示上下文感知对话"""
    print("=" * 70)
    print("上下文感知对话演示")
    print("=" * 70)

    # 初始化路由器
    router = ContextualDialogRouter(
        "data/models/router_hybrid/best_model.pth",  # 使用混合模型
        device="cuda" if torch.cuda.is_available() else "cpu",
        history_len=5
    )

    # 模拟对话场景
    scenarios = [
        {
            "name": "场景1：动作+对象分两次说",
            "user_id": "user1",
            "inputs": [
                "调一调",
                "温度",
            ]
        },
        {
            "name": "场景2：确认操作",
            "user_id": "user2",
            "inputs": [
                "打开空调",
                "好的",
            ]
        },
        {
            "name": "场景3：多轮细化",
            "user_id": "user3",
            "inputs": [
                "调节座椅",
                "左前",
                "加热",
            ]
        },
        {
            "name": "场景4：独立指令（无上下文）",
            "user_id": "user4",
            "inputs": [
                "导航到天安门",
            ]
        },
    ]

    for scenario in scenarios:
        print(f"\n{'=' * 70}")
        print(f"{scenario['name']}")
        print(f"{'=' * 70}")

        router.clear_history(scenario['user_id'])

        for i, user_input in enumerate(scenario['inputs'], 1):
            print(f"\n[用户 {i}] {user_input}")

            result = router.process_input(user_input, scenario['user_id'])

            print(f"[系统] {result['response']}")
            if result['used_context']:
                print(f"  (使用上下文: \"{result['original_input']}\" → \"{result['combined_input']}\")")
            print(f"  类别: {result['category']}, 置信度: {result['confidence']:.2f}")


if __name__ == "__main__":
    demo_contextual_dialog()
