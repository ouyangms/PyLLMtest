"""
Claude API 客户端
使用 Anthropic Claude API 生成训练样本
"""

import os
import json
from typing import List, Dict, Optional

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class ClaudeClient:
    """Claude API 客户端"""

    def __init__(
        self,
        api_key: str = None,
        model: str = "claude-3-haiku-20240307"  # 默认使用 Haiku（更快更便宜）
    ):
        """
        初始化 Claude 客户端

        Args:
            api_key: Anthropic API Key
            model: 模型名称 (haiku/sonnet/opus)
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("需要安装 anthropic: pip install anthropic")

        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError(
                "需要设置 ANTHROPIC_API_KEY 环境变量\n"
                "获取 API Key: https://console.anthropic.com/settings/keys"
            )

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.api_key = api_key

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        生成文本

        Args:
            prompt: 提示词
            max_tokens: 最大 token 数
            temperature: 温度参数

        Returns:
            生成的文本
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.content[0].text

        except Exception as e:
            raise RuntimeError(f"Claude API 调用失败: {e}")

    def generate_queries(
        self,
        skill_name: str,
        skill_description: str,
        existing_queries: List[str],
        target_count: int = 8
    ) -> List[str]:
        """
        为技能生成训练样本

        Args:
            skill_name: 技能名称
            skill_description: 技能描述
            existing_queries: 现有样本
            target_count: 目标数量

        Returns:
            生成的样本列表
        """
        needed = max(0, target_count - len(existing_queries))

        if needed <= 0:
            return existing_queries

        # 构建系统提示
        system_prompt = """你是一个专业的车载语音指令助手。你的任务是为车控技能生成多样化的用户表达方式。

生成规则：
1. 必须生成 5 种类型的表达（每种至少 1 条）：
   - A. 标准指令型：如"打开空调"
   - B. 场景/感受型：如"车里太热了"
   - C. 模糊/口语型：如"开一下""弄一下"
   - D. 否定/反向型：如"别吹风了"
   - E. 组合/上下文型：如"先开窗"

2. 质量要求：
   - 拒绝机器人式表达（如"请帮我..."）
   - 使用真实用户的口语化表达
   - 每条表达简洁（不超过 10 个字）
   - 覆盖不同方言和俗称

3. 输出格式：
   直接输出 JSON 数组，不要包含其他内容
   ["表达1", "表达2", ...]"""

        # 构建用户提示
        user_prompt = f"""请为以下车载技能生成 {needed} 条不同的用户表达。

技能名称: {skill_name}
技能描述: {skill_description}
现有样本: {', '.join(existing_queries[:3])}

请生成 {needed} 条新的表达，确保覆盖 5 种类型（标准指令、场景感受、模糊口语、否定反向、组合上下文）。

只返回 JSON 数组，不要包含其他内容。"""

        try:
            # 使用 Haiku 快速生成
            response = self.generate(
                prompt=user_prompt,
                max_tokens=800,
                temperature=0.8
            )

            # 解析响应
            queries = self._parse_response(response)

            if queries:
                # 合并去重
                seen = set(existing_queries)
                final_queries = list(existing_queries)

                for q in queries:
                    q = q.strip()
                    if q and q not in seen:
                        seen.add(q)
                        final_queries.append(q)

                return final_queries
            else:
                # 解析失败，返回原有样本
                return existing_queries

        except Exception as e:
            print(f"  [错误] {e}")
            return existing_queries

    def _parse_response(self, response: str) -> List[str]:
        """解析 Claude 响应"""
        queries = []

        # 尝试解析 JSON
        try:
            # 尝试直接解析
            data = json.loads(response)
            if isinstance(data, list):
                queries = [str(q).strip() for q in data if q]
        except json.JSONDecodeError:
            # 尝试提取 JSON 部分
            try:
                start = response.find("[")
                end = response.rfind("]") + 1
                if start >= 0 and end > start:
                    json_str = response[start:end]
                    data = json.loads(json_str)
                    queries = [str(q).strip() for q in data if q]
            except:
                pass

        # 如果 JSON 解析失败，尝试按行解析
        if not queries:
            lines = response.strip().split("\n")
            for line in lines:
                line = line.strip()
                # 跳过空行、标记行
                if not line or line.startswith("#") or line.startswith("//"):
                    continue
                # 移除序号前缀
                line = line.lstrip("0123456789.-、) ")
                if line and len(line) <= 20:
                    queries.append(line)

        return queries

    def batch_generate(
        self,
        skills: List[Dict],
        target_count: int = 8,
        batch_size: int = 10,
        start_index: int = 0,
        callback=None
    ) -> List[Dict]:
        """
        批量生成样本

        Args:
            skills: 技能列表
            target_count: 目标样本数
            batch_size: 批次大小
            start_index: 起始索引
            callback: 进度回调函数

        Returns:
            增强后的技能列表
        """
        enhanced_skills = []

        for i, skill in enumerate(skills[start_index:], start=start_index):
            skill_copy = skill.copy()
            existing_count = len(skill.get("example_queries", []))

            if callback:
                callback(i, len(skills), skill)

            if existing_count >= target_count:
                skill_copy["example_queries"] = skill["example_queries"]
            else:
                queries = self.generate_queries(
                    skill_name=skill["name"],
                    skill_description=skill["description"],
                    existing_queries=skill.get("example_queries", []),
                    target_count=target_count
                )
                skill_copy["example_queries"] = queries

            enhanced_skills.append(skill_copy)

            # 定期保存
            if (i + 1) % batch_size == 0 and callback:
                callback(i, len(skills), None, save=True)

        return enhanced_skills


def get_model_info() -> Dict[str, Dict]:
    """获取 Claude 模型信息"""
    return {
        "claude-3-haiku-20240307": {
            "name": "Claude 3 Haiku",
            "description": "最快最经济的模型，适合批量生成",
            "max_tokens": 200000,
            "input_price": 0.25,  # per 1M tokens
            "output_price": 1.25,  # per 1M tokens
            "speed": "最快"
        },
        "claude-3-5-sonnet-20241022": {
            "name": "Claude 3.5 Sonnet",
            "description": "平衡性能和速度",
            "max_tokens": 200000,
            "input_price": 3.0,
            "output_price": 15.0,
            "speed": "中等"
        },
        "claude-3-opus-20240229": {
            "name": "Claude 3 Opus",
            "description": "最高质量，但较慢",
            "max_tokens": 200000,
            "input_price": 15.0,
            "output_price": 75.0,
            "speed": "较慢"
        }
    }


def main():
    """测试 Claude 客户端"""
    import argparse

    parser = argparse.ArgumentParser(description="Claude API 客户端测试")
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-haiku-20240307",
        choices=["claude-3-haiku-20240307", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
        help="Claude 模型"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="测试模式"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Claude API 客户端测试")
    print("=" * 60)

    try:
        client = ClaudeClient(model=args.model)
        print(f"\n已连接到 Claude: {args.model}")

        if args.test:
            # 测试生成
            test_queries = client.generate_queries(
                skill_name="OpenAirCondition",
                skill_description="打开空调",
                existing_queries=["打开空调"],
                target_count=8
            )

            print(f"\n生成了 {len(test_queries)} 条样本:")
            for i, q in enumerate(test_queries, 1):
                print(f"  {i}. {q}")

    except Exception as e:
        print(f"\n错误: {e}")
        print("\n请确保:")
        print("1. 已安装 anthropic: pip install anthropic")
        print("2. 已设置 ANTHROPIC_API_KEY 环境变量")
        print("3. 有足够的 API 额度")


if __name__ == "__main__":
    main()
