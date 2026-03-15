"""
测试通义千问 API 生成训练样本
"""

import os
import json
import requests
import time
from pathlib import Path


def generate_qwen_samples(skill_name, skill_description, existing_queries, target_count=8):
    """使用通义千问生成样本"""

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("需要设置 DASHSCOPE_API_KEY 环境变量")

    needed = max(0, target_count - len(existing_queries))
    if needed <= 0:
        return existing_queries

    # 构建提示
    prompt = f"""请为以下车载技能生成 {needed} 条不同的用户表达。

技能名称: {skill_name}
技能描述: {skill_description}
现有样本: {', '.join(existing_queries[:3])}

请生成 {needed} 条新的表达，确保覆盖 5 种类型（标准指令、场景感受、模糊口语、否定反向、组合上下文）。

只返回 JSON 数组，不要包含其他内容。"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "messages": [
            {"role": "system", "content": "你是一个专业的车载语音指令助手，擅长生成各种自然语言表达。"},
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
            # 尝试直接解析
            queries = json.loads(content)
            if isinstance(queries, list):
                generated = [str(q).strip() for q in queries if q]
            else:
                generated = []
        except:
            # 尝试提取 JSON 部分
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
            # 合并去重
            seen = set(existing_queries)
            final_queries = list(existing_queries)

            for q in generated:
                q = q.strip()
                if q and q not in seen:
                    seen.add(q)
                    final_queries.append(q)

            return final_queries
        else:
            return existing_queries

    except Exception as e:
        print(f"  [错误] {e}")
        return existing_queries


def main():
    print("=" * 60)
    print("通义千问 API 训练样本生成测试")
    print("=" * 60)

    # 测试 API key
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误: 未设置 DASHSCOPE_API_KEY 环境变量")
        return

    print(f"API Key: {api_key[:10]}...{api_key[-4:]}")

    # 测试生成
    test_skill = {
        "name": "OpenAirCondition",
        "description": "打开空调",
        "example_queries": ["打开空调"]
    }

    print(f"\n测试技能: {test_skill['name']}")
    print(f"描述: {test_skill['description']}")
    print(f"现有样本: {test_skill['example_queries']}")

    print("\n开始生成...")
    start_time = time.time()

    result = generate_qwen_samples(
        test_skill["name"],
        test_skill["description"],
        test_skill["example_queries"],
        target_count=8
    )

    elapsed = time.time() - start_time

    print(f"\n生成完成! (耗时 {elapsed:.1f}s)")
    print(f"生成样本数: {len(result)}")

    print("\n生成的样本:")
    for i, q in enumerate(result, 1):
        print(f"  {i}. {q}")


if __name__ == "__main__":
    main()
