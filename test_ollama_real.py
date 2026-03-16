#!/usr/bin/env python3
"""
测试真实的 Ollama Qwen3-1.7B 性能
"""

import sys
import time
import json
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.hybrid.llm_parser import HybridLLMEngine

def test_ollama_connection():
    """测试 Ollama 连接"""
    print("测试 Ollama 连接...")

    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("已安装的模型:")
            for model in models:
                name = model.get("name", "")
                size_mb = model.get("size", 0) / (1024*1024)
                print(f"  - {name}: {size_mb:.0f}MB")

            if any("qwen3" in m["name"] for m in models):
                print("\n✓ qwen3:1.7b 模型已安装")
                return True
            else:
                print("\n❌ qwen3:1.7b 模型未安装")
                print("请运行: ollama pull qwen3:1.7b")
                return False
        else:
            print(f"❌ Ollama API 返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到 Ollama: {e}")
        return False

def test_ollama_performance():
    """测试 Ollama 性能"""
    if not test_ollama_connection():
        return

    print("\n" + "=" * 60)
    print("测试 Ollama Qwen3-1.7B 性能")
    print("=" * 60)

    # 创建引擎
    engine = HybridLLMEngine({
        "use_local": True,
        "base_url": "http://localhost:11434",
        "model_name": "qwen3:1.7b"
    })

    # 测试用例
    test_cases = [
        {
            "input": "打开空调",
            "candidates": [
                {"skill_id": "OpenAC", "name": "打开空调", "description": "打开空调系统", "params_schema": {}, "similarity": 0.9},
                {"skill_id": "CloseAC", "name": "关闭空调", "description": "关闭空调系统", "params_schema": {}, "similarity": 0.1}
            ]
        },
        {
            "input": "空调温度设为24度",
            "candidates": [
                {"skill_id": "SetTemp", "name": "设置温度", "description": "设置空调温度", "params_schema": {"temperature": "integer"}, "similarity": 0.85},
                {"skill_id": "OpenAC", "name": "打开空调", "description": "打开空调系统", "params_schema": {}, "similarity": 0.6}
            ]
        },
        {
            "input": "打开左前车窗",
            "candidates": [
                {"skill_id": "OpenWindow", "name": "打开车窗", "description": "打开指定车窗", "params_schema": {"position": "string"}, "similarity": 0.9},
                {"skill_id": "CloseWindow", "name": "关闭车窗", "description": "关闭车窗", "params_schema": {}, "similarity": 0.1}
            ]
        }
    ]

    # 预热模型
    print("\n预热模型...")
    engine.parse("测试", [{"skill_id": "test", "name": "测试", "description": "测试用例", "params_schema": {}, "similarity": 0.5}])
    print("预热完成！")

    # 测试延迟
    print("\n测试延迟 (10次)...")
    latencies = []

    for i, test_case in enumerate(test_cases):
        print(f"\n--- 测试用例 {i+1} ---")
        print(f"输入: {test_case['input']}")

        start_time = time.time()
        result = engine.parse(test_case["input"], test_case["candidates"])
        end_time = time.time()

        latency = (end_time - start_time) * 1000
        latencies.append(latency)

        print(f"延迟: {latency:.2f}ms")
        print(f"置信度: {result.confidence:.2f}")
        print(f"结果: {result.skill_id}")
        print(f"参数: {result.parameters}")

    # 计算统计
    avg_latency = sum(latencies) / len(latencies)

    print(f"\nOllama 性能总结:")
    print(f"平均延迟: {avg_latency:.2f}ms")
    print(f"单个请求: {latencies}")

    # 判断性能等级
    if avg_latency < 300:
        grade = "优秀 (A+)"
    elif avg_latency < 500:
        grade = "良好 (A)"
    elif avg_latency < 1000:
        grade = "一般 (B)"
    else:
        grade = "较慢 (C)"

    print(f"性能等级: {grade}")

    # 保存结果
    results = {
        "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "provider": "ollama",
        "model": "qwen3:1.7b",
        "avg_latency_ms": avg_latency,
        "individual_latencies_ms": latencies,
        "performance_grade": grade
    }

    with open('ollama_performance_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存到 ollama_performance_results.json")

if __name__ == "__main__":
    test_ollama_performance()