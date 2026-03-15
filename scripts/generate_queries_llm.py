"""
使用 LLM API 生成高质量训练样本
"""

import json
import os
import time
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.llm_client import create_llm_client


# 五维度样本生成模板
QUERY_DIMENSIONS = {
    "standard": {
        "name": "标准指令型",
        "description": "清晰完整的指令表达，包含动作和对象",
        "examples": [
            "打开空调",
            "把座椅加热打开",
            "关闭所有车窗"
        ]
    },
    "scenario": {
        "name": "场景/感受型",
        "description": "描述当前状态或感受，隐含操作意图",
        "examples": [
            "车里太热了",
            "我想透透气",
            "腰有点酸",
            "外面太吵了"
        ]
    },
    "colloquial": {
        "name": "模糊/口语型",
        "description": "省略主语、使用方言或俗称、极简表达",
        "examples": [
            "开条缝",
            "透透气",
            "调高点",
            "声音大点",
            "弄一下"
        ]
    },
    "negative": {
        "name": "否定/反向型",
        "description": "通过否定表达来隐含操作",
        "examples": [
            "别吹风了",
            "太冷了，关掉",
            "不想要那么亮"
        ]
    },
    "context": {
        "name": "组合/上下文型",
        "description": "包含多个操作或依赖上下文",
        "examples": [
            "先把空调关了，再开窗",
            "还是开窗吧",
            "和刚才一样"
        ]
    }
}

# 车控领域同义词库（用于 Prompt）
SYNONYMS_CONTEXT = """
常见同义词对照:
- 空调: 冷气、暖气、风、AC、空气
- 车窗: 玻璃、窗户、窗
- 座椅: 座位、椅子、坐垫
- 后视镜: 镜子、耳朵、侧镜
- 打开: 开启、启动、开
- 关闭: 关掉、关上、关
- 调节: 调整、设置、设为、调
"""


def create_generation_prompt(skill: Dict, target_count: int = 8) -> str:
    """
    为技能创建样本生成 Prompt

    Args:
        skill: 技能信息
        target_count: 目标生成数量

    Returns:
        Prompt 字符串
    """
    name = skill.get("name", "")
    description = skill.get("description", "")
    existing = skill.get("example_queries", [])

    # 分析技能特征
    action = extract_action(description)
    obj = extract_object(description, name)

    prompt = f"""请为以下车载技能生成多样化的用户表达方式。

**技能信息:**
- 技能名称: {name}
- 技能描述: {description}
- 现有样本: {', '.join(existing[:3])}

**要求:**
1. 生成 {target_count} 条不同的用户表达
2. 必须包含以下 5 种类型（每种至少 1 条）:

   A. 标准指令型: 清晰完整的指令，如"{action}{obj}"
   B. 场景/感受型: 描述状态或感受，如"太热了""想透透气"
   C. 模糊/口语型: 省略主语、极简表达，如"开一下""弄一下"
   D. 否定/反向型: 通过否定表达意图，如"别吹风了"
   E. 组合/上下文型: 包含语境或连续操作

**注意事项:**
- 拒绝机器人式表达（如"请帮我..."）
- 使用真实用户的口语化表达
- 覆盖不同方言和俗称
- 处理指代不明的情况
- 每条表达必须简洁（不超过 10 个字）

{SYNONYMS_CONTEXT}

**输出格式:**
请直接输出 JSON 数组，不要包含其他内容:
[
  "表达1",
  "表达2",
  ...
]
"""

    return prompt


def extract_action(description: str) -> str:
    """从描述中提取动作"""
    desc_lower = description.lower()

    if "打开" in description or "open" in desc_lower or "开启" in description:
        return "打开"
    elif "关闭" in description or "close" in desc_lower or "关掉" in description:
        return "关闭"
    elif "调节" in description or "adjust" in desc_lower or "调整" in description:
        return "调节"
    elif "设置" in description or "set" in desc_lower:
        return "设置"
    else:
        return "操作"


def extract_object(description: str, name: str) -> str:
    """从描述中提取对象"""
    desc_lower = description.lower()
    name_lower = name.lower()

    keywords = {
        "空调": ["air", "空调", "冷气", "暖气", "ac"],
        "车窗": ["window", "车窗", "玻璃", "窗户"],
        "座椅": ["seat", "座椅", "座位", "椅子"],
        "灯": ["light", "灯", "灯光", "照明"],
        "后视镜": ["mirror", "后视镜", "镜子"],
        "音量": ["volume", "音量", "声音", "音乐"],
    }

    for obj, keys in keywords.items():
        if any(key in desc_lower or key in name_lower for key in keys):
            return obj

    return "设备"


def parse_llm_response(response: str) -> List[str]:
    """
    解析 LLM 响应，提取样本列表

    Args:
        response: LLM 返回的文本

    Returns:
        样本列表
    """
    queries = []

    # 尝试解析 JSON
    try:
        # 尝试直接解析
        data = json.loads(response)
        if isinstance(data, list):
            queries = [str(q).strip() for q in data if q]
        elif isinstance(data, dict) and "queries" in data:
            queries = [str(q).strip() for q in data["queries"] if q]
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


def generate_for_skill(
    skill: Dict,
    client,
    target_count: int = 8,
    max_retries: int = 3
) -> List[str]:
    """
    为单个技能生成样本

    Args:
        skill: 技能信息
        client: LLM 客户端
        target_count: 目标数量
        max_retries: 最大重试次数

    Returns:
        生成的样本列表
    """
    existing = skill.get("example_queries", [])
    needed = max(0, target_count - len(existing))

    if needed <= 0:
        return existing

    # 创建 Prompt
    prompt = create_generation_prompt(skill, needed)

    # 调用 LLM
    for attempt in range(max_retries):
        try:
            response = client.generate(
                prompt,
                max_tokens=1000,
                temperature=0.8
            )

            # 解析响应
            generated = parse_llm_response(response)

            if generated:
                # 合并去重
                seen = set(existing)
                final_queries = list(existing)

                for q in generated:
                    q = q.strip()
                    if q and q not in seen:
                        seen.add(q)
                        final_queries.append(q)

                return final_queries
            else:
                print(f"  [警告] 解析失败，重试 {attempt + 1}/{max_retries}")

        except Exception as e:
            print(f"  [错误] 生成失败: {e}，重试 {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(2)  # 等待后重试

    # 失败时返回原有样本
    return existing


def batch_generate(
    skills: List[Dict],
    client,
    target_count: int = 8,
    batch_size: int = 10,
    start_index: int = 0,
    resume_file: str = None
) -> List[Dict]:
    """
    批量生成样本

    Args:
        skills: 技能列表
        client: LLM 客户端
        target_count: 目标样本数
        batch_size: 批次大小
        start_index: 起始索引（用于断点续传）
        resume_file: 恢复文件路径

    Returns:
        增强后的技能列表
    """
    enhanced_skills = []

    # 如果有恢复文件，先加载
    if resume_file and Path(resume_file).exists():
        with open(resume_file, 'r', encoding='utf-8') as f:
            enhanced_skills = json.load(f)
        print(f"从恢复文件加载了 {len(enhanced_skills)} 个技能")

    stats = {
        "total": len(skills),
        "processed": len(enhanced_skills),
        "enhanced": 0,
        "failed": 0,
        "total_queries": 0
    }

    print(f"\n开始批量生成（从第 {start_index + 1} 个技能开始）")
    print(f"目标: 每个技能 {target_count} 条样本")
    print("-" * 60)

    for i, skill in enumerate(skills[start_index:], start=start_index):
        if i < len(enhanced_skills):
            continue

        skill_copy = skill.copy()
        existing_count = len(skill.get("example_queries", []))

        print(f"\n[{i + 1}/{len(skills)}] {skill['name'][:40]}")

        if existing_count >= target_count:
            print(f"  [跳过] 已有 {existing_count} 条样本")
            skill_copy["example_queries"] = skill["example_queries"]
        else:
            print(f"  [生成] {existing_count} -> {target_count} 条")
            start_time = time.time()

            try:
                # 生成样本
                queries = generate_for_skill(
                    skill_copy,
                    client,
                    target_count=target_count
                )

                skill_copy["example_queries"] = queries
                stats["enhanced"] += 1
                stats["total_queries"] += len(queries)

                elapsed = time.time() - start_time
                print(f"  [完成] 生成 {len(queries)} 条样本 ({elapsed:.1f}s)")

            except Exception as e:
                print(f"  [失败] {e}")
                stats["failed"] += 1
                skill_copy["example_queries"] = skill.get("example_queries", [])

        enhanced_skills.append(skill_copy)

        # 定期保存
        if (i + 1) % batch_size == 0 and resume_file:
            with open(resume_file, 'w', encoding='utf-8') as f:
                json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)
            print(f"\n[保存] 进度已保存到 {resume_file}")

    return enhanced_skills


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="LLM 训练样本生成器")
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/skills_database.json",
        help="输入技能文件"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/skills_llm_enhanced.json",
        help="输出文件"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        choices=["openai", "qwen", "deepseek", "ollama"],
        help="LLM 提供商"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="模型名称（默认使用各提供商默认模型）"
    )
    parser.add_argument(
        "--target-count",
        type=int,
        default=8,
        help="每个技能的目标样本数"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="批次大小（用于断点续传）"
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="起始索引（用于断点续传）"
    )
    parser.add_argument(
        "--resume-file",
        type=str,
        help="恢复文件路径"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="测试模式（只生成前 5 个技能）"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LLM 训练样本生成")
    print("=" * 60)

    # 检查输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return

    # 加载技能数据
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        skills = json.load(f)

    print(f"加载了 {len(skills)} 个技能")

    # 测试模式
    if args.test:
        print("\n[测试模式] 只处理前 5 个技能")
        skills = skills[:5]
        args.batch_size = 1

    # 创建 LLM 客户端
    print(f"\n连接 LLM 服务: {args.provider}")
    try:
        client = create_llm_client(
            provider=args.provider,
            model=args.model
        )
        print(f"模型: {client.model or '默认'}")
    except Exception as e:
        print(f"错误: {e}")
        print("\n请设置相应的 API key 环境变量:")
        print("  OpenAI: OPENAI_API_KEY")
        print("  通义千问: DASHSCOPE_API_KEY")
        print("  DeepSeek: DEEPSEEK_API_KEY")
        return

    # 设置恢复文件
    resume_file = args.resume_file
    if not resume_file:
        resume_file = str(Path(args.output).with_suffix(".tmp.json"))

    # 批量生成
    start_time = time.time()
    enhanced_skills = batch_generate(
        skills=skills,
        client=client,
        target_count=args.target_count,
        batch_size=args.batch_size,
        start_index=args.start_index,
        resume_file=resume_file
    )
    elapsed = time.time() - start_time

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)

    # 统计
    print("\n" + "=" * 60)
    print("生成完成")
    print("=" * 60)
    print(f"输出文件: {output_path}")
    print(f"总耗时: {elapsed:.1f}s")

    # 验证
    with open(output_path, 'r', encoding='utf-8') as f:
        enhanced = json.load(f)

    total_queries = sum(len(s.get("example_queries", [])) for s in enhanced)
    avg_queries = total_queries / len(enhanced)
    sufficient = sum(1 for s in enhanced if len(s.get("example_queries", [])) >= args.target_count)

    print(f"\n验证统计:")
    print(f"  总技能数: {len(enhanced)}")
    print(f"  总样本数: {total_queries}")
    print(f"  平均样本数: {avg_queries:.2f}")
    print(f"  满足目标: {sufficient}/{len(enhanced)} ({sufficient/len(enhanced)*100:.1f}%)")

    # 删除临时文件
    if Path(resume_file).exists():
        Path(resume_file).unlink()
        print(f"\n已删除临时文件: {resume_file}")


if __name__ == "__main__":
    main()
