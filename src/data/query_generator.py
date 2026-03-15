"""
LLM 泛化训练样本生成器
使用大语言模型为每个技能生成高质量的口语化训练样本
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
import time
import re


class QueryGenerator:
    """训练样本生成器"""

    # 5个维度的生成模板
    DIMENSIONS = {
        "standard": {
            "name": "标准指令型",
            "description": "用户清晰、完整地表达意图，接近技能定义",
            "count": 1,
            "prompt_template": "生成 1 条标准指令型用户表达，清晰完整地描述这个操作"
        },
        "scenario": {
            "name": "场景/感受型",
            "description": "用户描述状态或感受，而非直接指令",
            "count": 2,
            "prompt_template": "生成 2 条场景/感受型用户表达，用户通过描述当前状态、感受或需求来间接表达意图（如'太热了'、'车里烟味大'）"
        },
        "colloquial": {
            "name": "模糊/口语型",
            "description": "省略主语、使用方言词汇、叠词或极简表达",
            "count": 2,
            "prompt_template": "生成 2 条模糊/口语型用户表达，包含省略主语、极简表达、叠词或日常口语（如'开条缝'、'透透气'）"
        },
        "negative": {
            "name": "否定/反向型",
            "description": "边界情况和反向操作",
            "count": 1,
            "prompt_template": "生成 1 条否定/反向型用户表达，涉及边界情况或与反向操作的区分"
        },
        "context": {
            "name": "组合/上下文型",
            "description": "模拟多轮对话或组合指令",
            "count": 1,
            "prompt_template": "生成 1 条组合/上下文型用户表达，模拟多轮对话中的不完整句子或上下文依赖"
        }
    }

    # 车控领域同义词和俗称
    SYNONYMS = {
        "空调": ["冷气", "暖气", "风", "AC"],
        "车窗": ["玻璃", "窗户", "窗"],
        "后备箱": ["尾箱", "后盖", "行李箱"],
        "后视镜": ["镜子", "耳朵", "侧镜"],
        "打开": ["开启", "启动", "开"],
        "关闭": ["关掉", "关上", "关"],
        "主驾": ["驾驶员", "驾驶位", "左前"],
        "副驾": ["乘客", "副驾驶", "右前"],
        "二排": ["后排", "后面"],
        "调节": ["调整", "设置", "设为"],
    }

    def __init__(self, api_key: str = None, api_base: str = None, model: str = None):
        """
        初始化生成器

        Args:
            api_key: API密钥（可选，从环境变量读取）
            api_base: API基础URL
            model: 模型名称
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")

        # 检查是否可用
        self.available = bool(self.api_key)

    def generate_for_skill(
        self,
        skill_name: str,
        description: str,
        existing_queries: List[str] = None,
        target_count: int = 8
    ) -> List[str]:
        """
        为单个技能生成训练样本

        Args:
            skill_name: 技能名称
            description: 技能描述
            existing_queries: 已有的示例查询
            target_count: 目标总数量（默认8条）

        Returns:
            完整的示例查询列表（包含原有+新生成的）
        """
        existing_queries = existing_queries or []
        current_count = len(existing_queries)
        needed_count = max(0, target_count - current_count)

        if needed_count == 0:
            return existing_queries

        # 使用规则生成（无API调用）
        if not self.available:
            return self._generate_by_rules(
                skill_name, description, existing_queries, needed_count
            )

        # 使用LLM生成
        return self._generate_by_llm(
            skill_name, description, existing_queries, needed_count
        )

    def _generate_by_rules(
        self,
        skill_name: str,
        description: str,
        existing_queries: List[str],
        needed_count: int
    ) -> List[str]:
        """
        使用规则生成样本（无API调用时的后备方案）

        Args:
            skill_name: 技能名称
            description: 技能描述
            existing_queries: 已有查询
            needed_count: 需要生成的数量

        Returns:
            生成的查询列表
        """
        generated = list(existing_queries)

        # 从描述中提取关键信息
        desc_lower = description.lower()

        # 提取动作词
        actions = {
            "open": ["打开", "开启", "启动", "开"],
            "close": ["关闭", "关掉", "关上", "关"],
            "adjust": ["调节", "调整", "设置", "设为"],
            "query": ["查询", "问", "查看", "多少"],
        }

        # 提取对象
        objects = {
            "air conditioner": ["空调", "冷气", "风"],
            "window": ["车窗", "玻璃", "窗户", "窗"],
            "seat": ["座椅", "座位", "椅子"],
            "light": ["灯", "灯光", "照明"],
            "mirror": ["后视镜", "镜子", "耳朵"],
        }

        # 根据技能名称生成
        base_name = skill_name.lower()

        # 生成标准型
        if "open" in base_name or "open" in desc_lower:
            generated.append(f"打开{description.split('(')[0].strip()}")
        elif "close" in base_name or "close" in desc_lower:
            generated.append(f"关闭{description.split('(')[0].strip()}")

        # 生成场景型
        if "air" in base_name or "空调" in description:
            generated.extend(["有点热，开空调", "车里太闷了，透透气"])
        elif "window" in base_name or "窗" in description:
            generated.extend(["烟味太大了，开个窗", "想吹吹风"])

        # 生成口语型
        if len(generated) < needed_count + len(existing_queries):
            generated.append(f"帮我把{description.split('(')[0].strip()}弄一下")

        # 去重并返回
        seen = set()
        result = []
        for q in generated:
            if q and q not in seen:
                seen.add(q)
                result.append(q)

        return result[:needed_count]

    def _generate_by_llm(
        self,
        skill_name: str,
        description: str,
        existing_queries: List[str],
        needed_count: int
    ) -> List[str]:
        """
        使用LLM生成样本

        Args:
            skill_name: 技能名称
            description: 技能描述
            existing_queries: 已有查询
            needed_count: 需要生成的数量

        Returns:
            生成的查询列表
        """
        try:
            import openai
        except ImportError:
            print("警告: 未安装 openai 包，将使用规则生成")
            return self._generate_by_rules(skill_name, description, existing_queries, needed_count)

        generated = list(existing_queries)

        # 构建提示词
        existing_str = "\n".join([f"- {q}" for q in existing_queries]) if existing_queries else "无"

        prompt = f"""你是一个车载语音数据专家。

技能名称: {skill_name}
技能描述: {description}

已有的用户表达:
{existing_str}

请为这个技能生成 {needed_count} 条新的口语化用户表达。

要求:
1. 覆盖不同维度: 标准指令、场景感受（如'太热了'）、模糊口语（如'开条缝'）、否定反向
2. 拒绝机器人语言: 不要说'执行XXX操作'
3. 覆盖同义词和俗称: 如空调→冷气/风，车窗→玻璃/窗户
4. 处理指代不明: 包含省略主语的样本
5. 完全模拟真实人类口吻

请直接输出JSON列表格式:
[
  "用户表达1",
  "用户表达2",
  ...
]
"""

        try:
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个车载语音数据专家，擅长生成各种口语化的用户表达。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )

            content = response.choices[0].message.content.strip()

            # 尝试解析JSON
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                new_queries = json.loads(json_match.group())
                if isinstance(new_queries, list):
                    generated.extend(new_queries)

        except Exception as e:
            print(f"LLM生成失败 ({skill_name}): {e}")
            return self._generate_by_rules(skill_name, description, existing_queries, needed_count)

        # 去重
        seen = set(existing_queries)
        result = list(existing_queries)
        for q in generated:
            if q and q not in seen:
                seen.add(q)
                result.append(q)

        return result

    def generate_batch(
        self,
        skills: List[Dict],
        target_count: int = 8,
        batch_size: int = 10,
        delay: float = 0.5
    ) -> List[Dict]:
        """
        批量生成训练样本

        Args:
            skills: 技能列表
            target_count: 每个技能的目标数量
            batch_size: 每批处理的数量
            delay: 请求间隔（秒）

        Returns:
            更新后的技能列表
        """
        result = []

        for i, skill in enumerate(skills):
            if i % batch_size == 0:
                print(f"处理进度: {i}/{len(skills)}")

            skill_copy = skill.copy()
            existing = skill.get("example_queries", [])

            # 生成新样本
            new_queries = self.generate_for_skill(
                skill["name"],
                skill["description"],
                existing,
                target_count
            )

            skill_copy["example_queries"] = new_queries
            result.append(skill_copy)

            # 延迟避免请求过快
            if delay > 0:
                time.sleep(delay)

        print(f"处理完成: {len(skills)}/{len(skills)}")
        return result

    def save_queries(
        self,
        skills: List[Dict],
        output_path: str = None
    ) -> str:
        """
        保存生成的训练样本

        Args:
            skills: 技能列表
            output_path: 输出文件路径

        Returns:
            输出文件的完整路径
        """
        if output_path is None:
            output_path = Path(__file__).parent.parent.parent / "data" / "processed" / "skills_with_queries.json"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(skills, f, ensure_ascii=False, indent=2)

        print(f"已保存到: {output_path}")
        return str(output_path)

    def get_statistics(self, skills: List[Dict]) -> Dict[str, Any]:
        """
        获取统计信息

        Args:
            skills: 技能列表

        Returns:
            统计信息字典
        """
        stats = {
            "total_skills": len(skills),
            "total_queries": 0,
            "avg_queries": 0,
            "min_queries": float('inf'),
            "max_queries": 0,
            "skills_with_enough": 0,  # >= 8条
            "query_distribution": {},
        }

        all_counts = []
        for skill in skills:
            count = len(skill.get("example_queries", []))
            all_counts.append(count)
            stats["total_queries"] += count

            if count < stats["min_queries"]:
                stats["min_queries"] = count
            if count > stats["max_queries"]:
                stats["max_queries"] = count

            if count >= 8:
                stats["skills_with_enough"] += 1

            # 分布统计
            key = f"{count}条"
            stats["query_distribution"][key] = stats["query_distribution"].get(key, 0) + 1

        if stats["total_skills"] > 0:
            stats["avg_queries"] = stats["total_queries"] / stats["total_skills"]
        else:
            stats["min_queries"] = 0

        return stats


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="LLM泛化训练样本生成器")
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/skills_database.json",
        help="输入技能数据库文件"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/skills_with_queries.json",
        help="输出文件路径"
    )
    parser.add_argument(
        "--target-count",
        type=int,
        default=8,
        help="每个技能的目标样本数量"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API密钥"
    )
    parser.add_argument(
        "--api-base",
        type=str,
        help="API基础URL"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="LLM模型名称"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="批处理大小"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="请求间隔（秒）"
    )

    args = parser.parse_args()

    # 加载技能数据
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return

    print(f"加载技能数据: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        skills = json.load(f)

    print(f"加载了 {len(skills)} 个技能")

    # 创建生成器
    generator = QueryGenerator(
        api_key=args.api_key,
        api_base=args.api_base,
        model=args.model
    )

    if not generator.available:
        print("警告: 未配置API密钥，将使用规则生成（效果可能不如LLM）")
        print("提示: 设置 OPENAI_API_KEY 环境变量或使用 --api-key 参数")
    else:
        print(f"使用LLM生成: {generator.model}")

    # 批量生成
    print("\n开始生成训练样本...")
    print("=" * 60)

    skills = generator.generate_batch(
        skills,
        target_count=args.target_count,
        batch_size=args.batch_size,
        delay=args.delay
    )

    # 保存结果
    output_path = generator.save_queries(skills, args.output)

    # 打印统计
    print("\n" + "=" * 60)
    print("生成统计")
    print("=" * 60)

    stats = generator.get_statistics(skills)
    print(f"总技能数: {stats['total_skills']}")
    print(f"总样本数: {stats['total_queries']}")
    print(f"平均样本数: {stats['avg_queries']:.2f}")
    print(f"最少样本数: {stats['min_queries']}")
    print(f"最多样本数: {stats['max_queries']}")
    print(f"达标技能数 (≥{args.target_count}条): {stats['skills_with_enough']}")

    print("\n样本数量分布:")
    for key, count in sorted(stats["query_distribution"].items(), key=lambda x: int(x[0].replace("条", ""))):
        print(f"  {key}: {count} 个技能")

    print("=" * 60)
    print(f"完成! 结果已保存到: {output_path}")


if __name__ == "__main__":
    main()
