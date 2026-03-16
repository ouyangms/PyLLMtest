#!/usr/bin/env python3
"""
Qwen3-1.7B 性能详细测试
"""

import sys
import time
import json
import statistics
from pathlib import Path
from typing import List, Dict, Any
import threading
import concurrent.futures
import psutil

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.hybrid.llm_parser import HybridLLMEngine


class DetailedPerformanceTest:
    """详细的性能测试"""

    def __init__(self):
        self.test_cases = [
            {
                "name": "空调操作",
                "input": "打开空调",
                "candidates": [
                    {"skill_id": "OpenAC", "name": "打开空调", "description": "打开空调系统", "params_schema": {}, "similarity": 0.9},
                    {"skill_id": "SetTemp", "name": "设置温度", "description": "调节温度", "params_schema": {"temp": "int"}, "similarity": 0.7}
                ]
            },
            {
                "name": "车窗控制",
                "input": "打开左前车窗",
                "candidates": [
                    {"skill_id": "OpenWindow", "name": "打开车窗", "description": "打开指定车窗", "params_schema": {"pos": "str"}, "similarity": 0.9},
                    {"skill_id": "CloseWindow", "name": "关闭车窗", "description": "关闭车窗", "params_schema": {}, "similarity": 0.1}
                ]
            },
            {
                "name": "音量调节",
                "input": "调小一点音量",
                "candidates": [
                    {"skill_id": "VolumeDown", "name": "减小音量", "description": "降低音量", "params_schema": {}, "similarity": 0.8},
                    {"skill_id": "VolumeUp", "name": "增大音量", "description": "增大音量", "params_schema": {}, "similarity": 0.2}
                ]
            }
        ]

    def test_throughput(self, engine, iterations=1000):
        """测试吞吐量"""
        print(f"\n开始吞吐量测试（{iterations} 次请求）...")

        start_time = time.time()
        results = []

        for i in range(iterations):
            test_case = self.test_cases[i % len(self.test_cases)]
            result = engine.parse(
                test_case["input"],
                test_case["candidates"]
            )
            results.append(result)

            if i % 100 == 0:
                elapsed = time.time() - start_time
                throughput = i / elapsed
                print(f"已完成 {i}/{iterations}, 吞吐量: {throughput:.2f} req/s")

        total_time = time.time() - start_time
        throughput = iterations / total_time

        return {
            "total_requests": iterations,
            "total_time_s": total_time,
            "throughput_req_s": throughput,
            "avg_latency_ms": (total_time * 1000) / iterations,
            "results": results
        }

    def test_concurrent_performance(self, engine, max_workers=10, requests_per_worker=100):
        """测试并发性能"""
        print(f"\n开始并发性能测试（{max_workers} 个并发，每个 {requests_per_worker} 请求）...")

        def worker(worker_id, results):
            start_time = time.time()
            worker_results = []

            for i in range(requests_per_worker):
                test_case = self.test_cases[i % len(self.test_cases)]
                result = engine.parse(
                    test_case["input"],
                    test_case["candidates"]
                )
                worker_results.append({
                    "worker": worker_id,
                    "request": i,
                    "result": result,
                    "latency_ms": time.time() * 1000
                })

            worker_results[0]["start_time"] = start_time
            worker_results[-1]["end_time"] = time.time()
            results[worker_id] = worker_results

        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for worker_id in range(max_workers):
                future = executor.submit(worker, worker_id, results)
                futures.append(future)

            # 等待所有任务完成
            concurrent.futures.wait(futures)

        # 计算统计信息
        all_latencies = []
        total_requests = 0
        total_time = 0

        for worker_results in results.values():
            if worker_results:
                start_time = worker_results[0]["start_time"]
                end_time = worker_results[-1]["end_time"]
                worker_time = end_time - start_time
                total_time = max(total_time, worker_time)
                total_requests += len(worker_results)

                for result in worker_results:
                    if "latency_ms" in result:
                        # 计算相对延迟
                        latency = (result["latency_ms"] / 1000) - start_time
                        all_latencies.append(latency * 1000)

        return {
            "total_requests": total_requests,
            "total_time_s": total_time,
            "throughput_req_s": total_requests / total_time if total_time > 0 else 0,
            "avg_latency_ms": statistics.mean(all_latencies) if all_latencies else 0,
            "p95_latency_ms": statistics.quantiles(all_latencies, n=20)[18] if all_latencies else 0,
            "p99_latency_ms": statistics.quantiles(all_latencies, n=100)[98] if all_latencies else 0,
            "min_latency_ms": min(all_latencies) if all_latencies else 0,
            "max_latency_ms": max(all_latencies) if all_latencies else 0
        }

    def test_memory_usage(self, engine):
        """测试内存使用"""
        print("\n开始内存使用测试...")

        process = psutil.Process()
        initial_memory = process.memory_info().rss / (1024 ** 2)

        # 执行大量请求
        print("执行 1000 次请求以监控内存...")
        for i in range(1000):
            test_case = self.test_cases[i % len(self.test_cases)]
            engine.parse(test_case["input"], test_case["candidates"])

            if i % 200 == 0:
                current_memory = process.memory_info().rss / (1024 ** 2)
                print(f"请求 {i}: 内存使用 {current_memory:.2f}MB")

        final_memory = process.memory_info().rss / (1024 ** 2)
        memory_increase = final_memory - initial_memory

        return {
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_increase_mb": memory_increase
        }

    def test_accuracy(self, engine):
        """测试准确率"""
        print("\n开始准确率测试...")

        test_cases_with_ground_truth = [
            {
                "input": "打开空调",
                "expected_skill": "OpenAC",
                "candidates": [
                    {"skill_id": "OpenAC", "name": "打开空调", "description": "打开空调系统", "params_schema": {}, "similarity": 0.9},
                    {"skill_id": "CloseAC", "name": "关闭空调", "description": "关闭空调系统", "params_schema": {}, "similarity": 0.1}
                ]
            },
            {
                "input": "温度设为24度",
                "expected_skill": "SetTemp",
                "candidates": [
                    {"skill_id": "SetTemp", "name": "设置温度", "description": "调节温度", "params_schema": {"temp": "int"}, "similarity": 0.85},
                    {"skill_id": "OpenAC", "name": "打开空调", "description": "打开空调系统", "params_schema": {}, "similarity": 0.6}
                ]
            }
        ]

        correct = 0
        total = len(test_cases_with_ground_truth)

        for test_case in test_cases_with_ground_truth:
            result = engine.parse(test_case["input"], test_case["candidates"])
            if result.skill_id == test_case["expected_skill"]:
                correct += 1

        accuracy = correct / total
        print(f"正确预测: {correct}/{total}")

        return {
            "total_tests": total,
            "correct_predictions": correct,
            "accuracy": accuracy
        }

    def run_all_tests(self):
        """运行所有性能测试"""
        print("Qwen3-1.7B 详细性能测试")
        print("=" * 70)
        print(f"系统信息:")
        print(f"CPU: {psutil.cpu_count()} 核")
        print(f"内存: {psutil.virtual_memory().total / (1024**3):.2f}GB")
        print("=" * 70)

        # 创建引擎
        engine = HybridLLMEngine({"use_local": False})

        all_results = {}

        # 1. 吞吐量测试
        print("\n" + "=" * 50)
        print("1. 吞吐量测试")
        print("=" * 50)
        throughput_results = self.test_throughput(engine, iterations=1000)
        all_results["throughput"] = throughput_results
        print(f"吞吐量: {throughput_results['throughput_req_s']:.2f} req/s")
        print(f"平均延迟: {throughput_results['avg_latency_ms']:.2f}ms")

        # 2. 并发性能测试
        print("\n" + "=" * 50)
        print("2. 并发性能测试")
        print("=" * 50)
        concurrent_results = self.test_concurrent_performance(engine, max_workers=5, requests_per_worker=200)
        all_results["concurrent"] = concurrent_results
        print(f"并发吞吐量: {concurrent_results['throughput_req_s']:.2f} req/s")
        print(f"平均延迟: {concurrent_results['avg_latency_ms']:.2f}ms")
        print(f"P95延迟: {concurrent_results['p95_latency_ms']:.2f}ms")
        print(f"P99延迟: {concurrent_results['p99_latency_ms']:.2f}ms")

        # 3. 内存使用测试
        print("\n" + "=" * 50)
        print("3. 内存使用测试")
        print("=" * 50)
        memory_results = self.test_memory_usage(engine)
        all_results["memory"] = memory_results
        print(f"初始内存: {memory_results['initial_memory_mb']:.2f}MB")
        print(f"最终内存: {memory_results['final_memory_mb']:.2f}MB")
        print(f"内存增长: {memory_results['memory_increase_mb']:.2f}MB")

        # 4. 准确率测试
        print("\n" + "=" * 50)
        print("4. 准确率测试")
        print("=" * 50)
        accuracy_results = self.test_accuracy(engine)
        all_results["accuracy"] = accuracy_results
        print(f"准确率: {accuracy_results['accuracy']*100:.1f}%")

        # 保存结果
        with open('detailed_performance_results.json', 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

        print("\n详细测试完成！结果已保存到 detailed_performance_results.json")

        return all_results


if __name__ == "__main__":
    test = DetailedPerformanceTest()
    results = test.run_all_tests()

    # 打印摘要
    print("\n" + "=" * 70)
    print("性能测试摘要")
    print("=" * 70)
    print(f"吞吐量: {results['throughput']['throughput_req_s']:.2f} req/s")
    print(f"并发吞吐量: {results['concurrent']['throughput_req_s']:.2f} req/s")
    print(f"平均延迟: {results['concurrent']['avg_latency_ms']:.2f}ms")
    print(f"准确率: {results['accuracy']['accuracy']*100:.1f}%")
    print(f"内存增长: {results['memory']['memory_increase_mb']:.2f}MB")