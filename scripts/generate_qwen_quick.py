"""
通义千问快速测试 - 只处理前 10 个技能
"""

import json
import os
import requests
from pathlib import Path


def generate_samples(skill, api_key, target_count=8):
    """生成单个技能的样本"""
    existing = skill.get("example_queries", [])
    needed = max(0, target_count - len(existing))

    if needed <= 0:
        return existing

    prompt = f"""请为以下车载技能生成 {needed} 条不同的用户表达。

技能名称: {skill['name']}
技能描述: {skill['description']}
现有样本: {', '.join(existing[:3])}

要求覆盖 5 种类型（标准、场景、口语、否定、上下文），每条不超过 10 个字。
只返回 JSON 数组。"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "messages": [
            {"role": "system", "content": "你是车载语音指令助手。"},
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
        print(f"  Error: {e}")
        return existing


def main():
    print("=" * 60)
    print("通义千问快速测试 - 10 个技能")
    print("=" * 60)

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("Error: DASHSCOPE_API_KEY not set")
        return

    # 加载数据
    with open("data/processed/skills_database.json", "r", encoding="utf-8-sig") as f:
        skills = json.load(f)

    test_skills = skills[:10]
    print(f"\n处理 {len(test_skills)} 个技能...\n")

    results = []
    for i, skill in enumerate(test_skills, 1):
        print(f"[{i}/10] {skill['name'][:30]}")
        existing_count = len(skill.get("example_queries", []))

        skill_copy = skill.copy()
        queries = generate_samples(skill_copy, api_key, target_count=8)
        skill_copy["example_queries"] = queries

        print(f"  {existing_count} -> {len(queries)} 条\n")

        results.append(skill_copy)

    # 保存
    output = Path("data/processed/skills_qwen_test.json")
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 统计
    total = sum(len(s.get("example_queries", [])) for s in results)
    avg = total / len(results)
    sufficient = sum(1 for s in results if len(s.get("example_queries", [])) >= 8)

    print("=" * 60)
    print("测试完成")
    print("=" * 60)
    print(f"输出: {output}")
    print(f"总样本: {total}")
    print(f"平均: {avg:.2f} 条/技能")
    print(f"满足 8 条: {sufficient}/10 ({sufficient/10*100:.0f}%)")


if __name__ == "__main__":
    main()
