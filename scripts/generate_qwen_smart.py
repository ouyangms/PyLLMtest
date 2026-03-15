"""
智能样本生成 - 只对不足的技能使用 LLM 补充
"""

import json
import os
import requests
import time
from pathlib import Path


def generate_samples(skill, api_key, target_count=8):
    """使用通义千问生成样本"""
    existing = skill.get("example_queries", [])
    needed = max(0, target_count - len(existing))

    if needed <= 0:
        return existing

    # 从技能名称和描述推断动作和对象
    name = skill["name"]
    desc = skill.get("description", "")

    # 简化的提示词
    prompt = f"""技能名称: {name}
功能描述: {desc}

现有样本: {', '.join(existing[:5])}

请生成 {needed} 条新的用户表达，要求：
1. 口语化、真实用户会说的话
2. 每条不超过 10 个字
3. 包含标准指令、场景描述、口语表达等不同类型

只返回 JSON 数组格式。"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "messages": [
            {"role": "system", "content": "你是车载语音指令助手，擅长生成用户口语表达。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.8
    }

    try:
        response = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # 解析
        try:
            queries = json.loads(content)
            if isinstance(queries, list):
                generated = [str(q).strip() for q in queries if q]
            else:
                generated = []
        except:
            # 尝试提取
            try:
                start = content.find("[")
                end = content.rfind("]") + 1
                if start >= 0:
                    queries = json.loads(content[start:end])
                    generated = [str(q).strip() for q in queries if q]
                else:
                    generated = []
            except:
                generated = []

        if generated:
            seen = set(existing)
            final = list(existing)
            for q in generated:
                if q and q not in seen and len(q) <= 15:
                    seen.add(q)
                    final.append(q)
            return final

        return existing

    except Exception as e:
        print(f"  [错误] {e}")
        return existing


def main():
    print("=" * 60)
    print("智能样本生成 - 使用通义千问补充不足的样本")
    print("=" * 60)

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误: 未设置 DASHSCOPE_API_KEY")
        return

    # 使用已增强的数据
    input_file = Path("data/processed/skills_llm_input.json")
    with open(input_file, "r", encoding="utf-8") as f:
        skills = json.load(f)

    print(f"\n总技能数: {len(skills)}")

    # 统计需要补充的技能
    need_llm = []
    target_count = 8

    for skill in skills:
        count = len(skill.get("example_queries", []))
        if count < target_count:
            need_llm.append((skill, target_count - count))

    print(f"需要补充: {len(need_llm)} 个技能")
    print(f"已满足: {len(skills) - len(need_llm)} 个技能")

    if not need_llm:
        print("\n所有技能样本已足够，无需生成")
        return

    # 成本估算
    print(f"\n预估成本: ~{len(need_llm) * 0.01:.2f} CNY")

    # 开始生成
    print("\n开始生成...\n")

    results = []
    total_generated = 0
    errors = 0

    start_time = time.time()

    for i, (skill, needed) in enumerate(need_llm, 1):
        skill_copy = skill.copy()
        existing = len(skill.get("example_queries", []))

        print(f"[{i}/{len(need_llm)}] {skill['name'][:35]:35s} ({existing} -> {target_count})")

        new_queries = generate_samples(skill_copy, api_key, target_count)
        new_count = len(new_queries) - existing

        skill_copy["example_queries"] = new_queries
        results.append(skill_copy)
        total_generated += new_count

        if new_count < needed:
            errors += 1

        # 小延迟避免限流
        time.sleep(0.1)

    # 合并已满足的技能
    for skill in skills:
        if len(skill.get("example_queries", [])) >= target_count:
            results.append(skill)

    elapsed = time.time() - start_time

    # 保存
    output = Path("data/processed/skills_qwen_final.json")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 统计
    total_queries = sum(len(s.get("example_queries", [])) for s in results)
    avg = total_queries / len(results)
    sufficient = sum(1 for s in results if len(s.get("example_queries", [])) >= target_count)

    print("\n" + "=" * 60)
    print("生成完成")
    print("=" * 60)
    print(f"输出文件: {output}")
    print(f"处理时间: {elapsed:.1f}s")
    print(f"新增样本: {total_generated}")
    print(f"错误: {errors}")
    print(f"\n最终统计:")
    print(f"  总技能数: {len(results)}")
    print(f"  总样本数: {total_queries}")
    print(f"  平均: {avg:.2f} 条/技能")
    print(f"  满足目标: {sufficient}/{len(results)} ({sufficient/len(results)*100:.1f}%)")


if __name__ == "__main__":
    main()
