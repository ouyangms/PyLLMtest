"""
使用通义千问 API 批量生成高质量训练样本
"""

import json
import os
import requests
import time
from pathlib import Path
from typing import List, Dict


def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_section(text):
    print("\n" + "-" * 60)
    print(text)
    print("-" * 60)


def generate_qwen_samples(
    skill_name: str,
    skill_description: str,
    existing_queries: List[str],
    target_count: int = 8,
    api_key: str = None
) -> List[str]:
    """使用通义千问生成样本"""

    needed = max(0, target_count - len(existing_queries))
    if needed <= 0:
        return existing_queries

    # 构建提示
    prompt = f"""请为以下车载技能生成 {needed} 条不同的用户表达。

技能名称: {skill_name}
技能描述: {skill_description}
现有样本: {', '.join(existing_queries[:3])}

请生成 {needed} 条新的表达，确保覆盖 5 种类型：
- A. 标准指令型：如"打开空调"
- B. 场景/感受型：如"车里太热了""想透透气"
- C. 模糊/口语型：如"开一下""弄一下"
- D. 否定/反向型：如"别吹风了"
- E. 组合/上下文型：如"先开窗"

质量要求：
- 拒绝机器人式表达（如"请帮我..."）
- 使用真实用户的口语化表达
- 每条表达简洁（不超过 10 个字）

只返回 JSON 数组，不要包含其他内容。"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的车载语音指令助手，擅长生成各种自然语言表达。"
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.8
    }

    try:
        response = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # 解析 JSON
        try:
            queries = json.loads(content)
            if isinstance(queries, list):
                generated = [str(q).strip() for q in queries if q]
            else:
                generated = []
        except:
            try:
                start = content.find("[")
                end = content.rfind("]") + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    queries = json.loads(json_str)
                    generated = [str(q).strip() for q in queries if q]
                else:
                    generated = []
            except:
                generated = []

        if generated:
            seen = set(existing_queries)
            final_queries = list(existing_queries)

            for q in generated:
                q = q.strip()
                if q and q not in seen and len(q) <= 15:
                    seen.add(q)
                    final_queries.append(q)

            return final_queries
        else:
            return existing_queries

    except Exception as e:
        print(f"  [错误] {e}")
        return existing_queries


def batch_generate(
    skills: List[Dict],
    api_key: str,
    target_count: int = 8,
    batch_size: int = 10,
    start_index: int = 0,
    output_file: str = None
) -> List[Dict]:
    """批量生成样本"""

    enhanced_skills = []

    print_section(f"开始批量生成（从第 {start_index + 1} 个技能开始）")
    print(f"目标: 每个技能 {target_count} 条样本")
    print(f"批处理大小: {batch_size}")

    start_time = time.time()
    last_save_time = start_time

    for i, skill in enumerate(skills[start_index:], start=start_index):
        skill_copy = skill.copy()
        existing = skill.get("example_queries", [])
        existing_count = len(existing)

        print(f"\n[{i+1}/{len(skills)}] {skill['name'][:40]}")

        if existing_count >= target_count:
            print(f"  [跳过] 已有 {existing_count} 条")
            skill_copy["example_queries"] = existing
        else:
            print(f"  [生成] {existing_count} -> {target_count} 条")
            gen_start = time.time()

            queries = generate_qwen_samples(
                skill["name"],
                skill["description"],
                existing,
                target_count=target_count,
                api_key=api_key
            )

            gen_time = time.time() - gen_start
            new_count = len(queries) - existing_count
            print(f"  [完成] 新增 {new_count} 条，共 {len(queries)} 条 ({gen_time:.1f}s)")

            skill_copy["example_queries"] = queries

        enhanced_skills.append(skill_copy)

        # 定期保存
        current_time = time.time()
        if (i + 1) % batch_size == 0 or (current_time - last_save_time) > 60:
            if output_file:
                temp_path = Path(output_file).with_suffix(".tmp.json")
                temp_path.parent.mkdir(parents=True, exist_ok=True)

                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)

                last_save_time = current_time
                print(f"  [保存] 进度已保存 ({i+1}/{len(skills)})")

    return enhanced_skills


def main():
    print_header("通义千问 API 训练样本生成")

    # 获取 API key
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误: 未设置 DASHSCOPE_API_KEY 环境变量")
        print("\n请设置:")
        print("  set DASHSCOPE_API_KEY=your-key-here")
        return

    print(f"API Key: {api_key[:10]}...{api_key[-4:]}")

    # 加载数据
    input_path = Path("data/processed/skills_database.json")
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8-sig') as f:
        skills = json.load(f)

    print(f"\n输入文件: {input_path}")
    print(f"技能数量: {len(skills)}")

    # 估算成本
    print_section("成本估算")
    avg_input_tokens = 200  # 每个技能平均输入 tokens
    avg_output_tokens = target_count = 8 * 10  # 每个技能平均输出 tokens

    total_input = len(skills) * avg_input_tokens
    total_output = len(skills) * avg_output_tokens

    # qwen-turbo 价格
    input_price = 0.0008  # CNY per 1K tokens
    output_price = 0.002  # CNY per 1K tokens

    input_cost = (total_input / 1000) * input_price
    output_cost = (total_output / 1000) * output_price
    total_cost = input_cost + output_cost

    print(f"预估 tokens:")
    print(f"  输入: {total_input:,}")
    print(f"  输出: {total_output:,}")
    print(f"  总计: {total_input + total_output:,}")
    print(f"\n预估成本 (CNY):")
    print(f"  输入: {input_cost:.2f}")
    print(f"  输出: {output_cost:.2f}")
    print(f"  总计: {total_cost:.2f}")

    # 开始生成
    print_section("准备开始")
    output_file = "data/processed/skills_qwen_enhanced.json"

    try:
        enhanced_skills = batch_generate(
            skills=skills,
            api_key=api_key,
            target_count=8,
            batch_size=20,
            output_file=output_file
        )

        # 保存结果
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)

        elapsed = time.time() - start_time

        # 验证
        with open(output_path, 'r', encoding='utf-8') as f:
            final_skills = json.load(f)

        total_queries = sum(len(s.get("example_queries", [])) for s in final_skills)
        avg_queries = total_queries / len(final_skills)
        sufficient = sum(1 for s in final_skills if len(s.get("example_queries", [])) >= 8)

        print_section("生成完成")
        print(f"输出文件: {output_path}")
        print(f"总耗时: {elapsed:.1f}s ({elapsed/60:.1f} 分钟)")

        print(f"\n验证统计:")
        print(f"  总技能数: {len(final_skills)}")
        print(f"  总样本数: {total_queries}")
        print(f"  平均样本数: {avg_queries:.2f}")
        print(f"  满足目标: {sufficient}/{len(final_skills)} ({sufficient/len(final_skills)*100:.1f}%)")

        # 删除临时文件
        temp_path = Path(output_file).with_suffix(".tmp.json")
        if temp_path.exists():
            temp_path.unlink()

    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消操作")
        print(f"\n进度已保存到: {output_file}.tmp.json")
        print(f"使用 --start-index {len(enhanced_skills)} 恢复")

    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
