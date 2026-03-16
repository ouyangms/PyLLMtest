#!/usr/bin/env python3
"""
简化的 Qwen3-1.7B 性能测试
"""

import sys
import time
import json
import statistics
from pathlib import Path
from typing import List, Dict, Any
import psutil

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.hybrid.llm_parser import HybridLLMEngine


def run_performance_test():
    """运行性能测试"""
    print("Qwen3-1.7B 简化性能测试")
    print("=" * 60)

    # 系统信息
    print(f"系统信息:")
    print(f"CPU: {psutil.cpu_count()} 核")
    print(f"内存: {psutil.virtual_memory().total / (1024**3):.2f}GB")
    print("=" * 60)

    # 创建引擎
    engine = HybridLLMEngine({"use_local": False})

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
                {"skill_id": "SetTemp", "name": "设置温度", "description": "设置空调温度", "params_schema": {"temp": "int"}, "similarity": 0.85},
                {"skill_id": "OpenAC", "name": "打开空调", "description": "打开空调系统", "params_schema": {}, "similarity": 0.6}
            ]
        },
        {
            "input": "打开左前车窗",
            "candidates": [
                {"skill_id": "OpenWindow", "name": "打开车窗", "description": "打开指定车窗", "params_schema": {"pos": "str"}, "similarity": 0.9},
                {"skill_id": "CloseWindow", "name": "关闭车窗", "description": "关闭车窗", "params_schema": {}, "similarity": 0.1}
            ]
        }
    ]

    # 1. 基础延迟测试
    print("\n1. 基础延迟测试 (100次)")
    print("-" * 40)
    latencies = []

    for i in range(100):
        test_case = test_cases[i % len(test_cases)]
        start_time = time.perf_counter()
        result = engine.parse(test_case["input"], test_case["candidates"])
        end_time = time.perf_counter()

        latency = (end_time - start_time) * 1000  # 转换为毫秒
        latencies.append(latency)

        if i < 3:  # 只打印前几次
            print(f"请求 {i+1}: {latency:.3f}ms - {result.skill_id}")

    # 计算统计
    avg_latency = statistics.mean(latencies)
    p95_latency = statistics.quantiles(latencies, n=20)[18]
    p99_latency = statistics.quantiles(latencies, n=100)[98]
    min_latency = min(latencies)
    max_latency = max(latencies)

    print(f"\n延迟统计:")
    print(f"平均: {avg_latency:.3f}ms")
    print(f"P95:  {p95_latency:.3f}ms")
    print(f"P99:  {p99_latency:.3f}ms")
    print(f"最小: {min_latency:.3f}ms")
    print(f"最大: {max_latency:.3f}ms")

    # 2. 内存使用测试
    print(f"\n2. 内存使用测试")
    print("-" * 40)

    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 ** 2)
    print(f"初始内存: {initial_memory:.2f}MB")

    # 执行大量请求
    print("执行 1000 次请求...")
    for i in range(1000):
        test_case = test_cases[i % len(test_cases)]
        engine.parse(test_case["input"], test_case["candidates"])

        if i % 250 == 0:
            current_memory = process.memory_info().rss / (1024 ** 2)
            print(f"请求 {i}: 内存 {current_memory:.2f}MB")

    final_memory = process.memory_info().rss / (1024 ** 2)
    memory_increase = final_memory - initial_memory

    print(f"最终内存: {final_memory:.2f}MB")
    print(f"内存增长: {memory_increase:.2f}MB")
    print(f"内存增长率: {(memory_increase/initial_memory)*100:.1f}%")

    # 3. 简单吞吐量测试
    print(f"\n3. 吞吐量测试")
    print("-" * 40)

    # 测试 10秒能处理多少请求
    start_time = time.time()
    count = 0
    test_end = start_time + 10  # 10秒

    while time.time() < test_end:
        test_case = test_cases[count % len(test_cases)]
        engine.parse(test_case["input"], test_case["candidates"])
        count += 1

    actual_time = time.time() - start_time
    throughput = count / actual_time

    print(f"测试时长: {actual_time:.2f}秒")
    print(f"请求数量: {count}")
    print(f"吞吐量: {throughput:.2f} req/s")

    # 4. 准确率测试
    print(f"\n4. 准确率测试")
    print("-" * 40)

    test_cases_with_ground_truth = [
        {
            "input": "打开空调",
            "expected": "OpenAC",
            "candidates": [
                {"skill_id": "OpenAC", "name": "打开空调", "similarity": 0.9},
                {"skill_id": "CloseAC", "name": "关闭空调", "similarity": 0.1}
            ]
        },
        {
            "input": "温度调低",
            "expected": "SetTemp",
            "candidates": [
                {"skill_id": "SetTemp", "name": "设置温度", "similarity": 0.85},
                {"skill_id": "OpenAC", "name": "打开空调", "similarity": 0.6}
            ]
        }
    ]

    correct = 0
    for test_case in test_cases_with_ground_truth:
        result = engine.parse(test_case["input"], test_case["candidates"])
        if result.skill_id == test_case["expected"]:
            correct += 1
        print(f"'{test_case['input']}' -> {result.skill_id} (期望: {test_case['expected']})")

    accuracy = correct / len(test_cases_with_ground_truth)
    print(f"\n准确率: {accuracy*100:.1f}% ({correct}/{len(test_cases_with_ground_truth)})")

    # 保存结果
    results = {
        "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": {
            "cpu_cores": psutil.cpu_count(),
            "total_memory_gb": psutil.virtual_memory().total / (1024**3)
        },
        "latency": {
            "avg_ms": avg_latency,
            "p95_ms": p95_latency,
            "p99_ms": p99_latency,
            "min_ms": min_latency,
            "max_ms": max_latency
        },
        "throughput": {
            "req_per_sec": throughput,
            "requests_10s": count
        },
        "memory": {
            "initial_mb": initial_memory,
            "final_mb": final_memory,
            "increase_mb": memory_increase,
            "increase_percent": (memory_increase/initial_memory)*100
        },
        "accuracy": {
            "score": accuracy,
            "correct": correct,
            "total": len(test_cases_with_ground_truth)
        }
    }

    with open('simple_performance_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n测试完成！结果已保存到 simple_performance_results.json")

    # 性能评级
    print("\n" + "=" * 60)
    print("性能评估")
    print("=" * 60)

    if avg_latency < 10:
        latency_grade = "优秀 (A+)"
    elif avg_latency < 50:
        latency_grade = "良好 (A)"
    elif avg_latency < 100:
        latency_grade = "一般 (B)"
    else:
        latency_grade = "较差 (C)"

    if throughput > 100:
        throughput_grade = "优秀 (A+)"
    elif throughput > 50:
        throughput_grade = "良好 (A)"
    elif throughput > 20:
        throughput_grade = "一般 (B)"
    else:
        throughput_grade = "较差 (C)"

    print(f"延迟性能: {latency_grade} ({avg_latency:.3f}ms)")
    print(f"吞吐量性能: {throughput_grade} ({throughput:.2f} req/s)")
    print(f"内存稳定性: {'优秀' if memory_increase < 10 else '一般'} (+{memory_increase:.2f}MB)")
    print(f"准确率: {accuracy*100:.1f}%")

    if accuracy > 0.8 and avg_latency < 50 and throughput > 50:
        print("\n🎯 总体评价: 符合高性能车控系统要求！")
    else:
        print("\n⚠️  总体评价: 需要进一步优化")


if __name__ == "__main__":
    run_performance_test()