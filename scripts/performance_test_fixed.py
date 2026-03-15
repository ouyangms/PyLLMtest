"""
车控技能路由系统 - 完整性能测试 (修复版)
修复路由分类延迟计算问题（批次延迟 vs 单样本延迟）
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict
from dataclasses import dataclass, asdict
import numpy as np

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig
from src.router.contextual_dialog import ContextualDialogRouter
from src.hybrid.inference_engine import InferenceEngine
from src.hybrid.skill_retriever import SkillRetriever, Skill
from src.hybrid.llm_parser import LLMParser


@dataclass
class TestResult:
    """测试结果"""
    stage: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    total_samples: int
    correct_samples: int
    per_category_stats: Dict[str, Dict[str, float]]


class PerformanceTester:
    """性能测试器 (修复版)"""

    def __init__(self, test_data_path: str):
        """初始化测试器"""
        print("=" * 70)
        print("车控技能路由系统 - 性能测试 (修复版)")
        print("=" * 70)

        # 加载测试数据
        print(f"\n加载测试数据: {test_data_path}")
        with open(test_data_path, "r", encoding="utf-8") as f:
            self.test_data = json.load(f)

        print(f"测试样本数: {len(self.test_data)}")

        # 统计类别分布
        from collections import Counter
        self.category_dist = Counter([
            item.get("category_name", item.get("category", ""))
            for item in self.test_data
        ])

        print(f"类别数: {len(self.category_dist)}")
        print("\n类别分布:")
        for cat, count in sorted(self.category_dist.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:20s}: {count:4d}")

        # 初始化各个组件
        self._init_components()

    def _init_components(self):
        """初始化测试组件"""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"\n使用设备: {device}")

        # 1. 路由模型
        print("加载路由模型...")
        vocab = CategoryConfig.create_vocabulary()
        self.router_model = TextCNNLite(len(vocab), num_classes=13)
        self.router_model.load_state_dict(
            torch.load("data/models/router_clean_final/best_model.pth", map_location=device)
        )
        self.router_model.to(device)
        self.router_model.eval()
        self.vocab = vocab
        self.device = device
        print("  [OK] 路由模型加载完成")

    def test_router_stage(self, num_samples: int = None) -> TestResult:
        """测试路由分类阶段 (修复版：单样本延迟)"""
        print("\n" + "=" * 70)
        print("阶段1: 路由分类测试 (单样本延迟)")
        print("=" * 70)

        if num_samples:
            test_data = self.test_data[:num_samples]
        else:
            test_data = self.test_data

        # 测试 - 单样本模式
        latencies = []
        category_stats = defaultdict(lambda: {"correct": 0, "total": 0})

        print(f"测试模式: 单样本测试 (真实延迟)")
        print(f"测试样本数: {len(test_data)}")

        with torch.no_grad():
            for item in test_data:
                # 编码
                indices = []
                for char in item["text"][:64]:
                    idx = self.vocab.get(char, self.vocab.get("<UNK>", 1))
                    indices.append(idx)

                if len(indices) < 64:
                    indices.extend([self.vocab.get("<PAD>", 0)] * (64 - len(indices)))

                indices_tensor = torch.tensor([indices], dtype=torch.long).to(self.device)

                # 预测 - 单样本
                start = time.perf_counter()
                outputs = self.router_model(indices_tensor)
                latency = (time.perf_counter() - start) * 1000

                _, predicted = torch.max(outputs, 1)
                predicted = predicted.item()

                # 统计
                true_label = item["category_id"]
                true_cat = CategoryConfig.CATEGORIES[true_label]
                pred_cat = CategoryConfig.CATEGORIES[predicted]

                category_stats[true_cat]["total"] += 1
                if true_label == predicted:
                    category_stats[true_cat]["correct"] += 1

                latencies.append(latency)

                # 进度显示
                if len(latencies) % 50 == 0:
                    print(f"  已测试: {len(latencies)}/{len(test_data)}")

        # 计算指标
        latencies = np.array(latencies)

        total_correct = sum(s["correct"] for s in category_stats.values())
        total_samples = sum(s["total"] for s in category_stats.values())
        accuracy = total_correct / total_samples if total_samples > 0 else 0

        # 计算每个类别的指标
        per_category_stats = {}
        for cat, stats in category_stats.items():
            if stats["total"] > 0:
                per_category_stats[cat] = {
                    "accuracy": stats["correct"] / stats["total"],
                    "precision": stats["correct"] / stats["total"],
                    "recall": stats["correct"] / stats["total"],
                    "f1": stats["correct"] / stats["total"],
                    "samples": stats["total"]
                }

        # 总体precision/recall/F1
        precision = accuracy
        recall = accuracy
        f1 = accuracy

        result = TestResult(
            stage="路由分类",
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1,
            avg_latency_ms=float(np.mean(latencies)),
            p50_latency_ms=float(np.percentile(latencies, 50)),
            p95_latency_ms=float(np.percentile(latencies, 95)),
            p99_latency_ms=float(np.percentile(latencies, 99)),
            total_samples=total_samples,
            correct_samples=total_correct,
            per_category_stats=per_category_stats
        )

        self._print_test_results(result)
        return result

    def test_retrieval_stage(self, top_k: int = 3) -> TestResult:
        """测试技能检索阶段"""
        print("\n" + "=" * 70)
        print("阶段2: 技能检索测试")
        print("=" * 70)

        # 初始化检索器
        skills_dir = Path("E:/ai/py/whisperModel/vc/skills")
        retriever = SkillRetriever(skills_dir, use_vector=False)

        total_skills = retriever.get_all_skills_count()
        print(f"技能总数: {total_skills}")

        # 创建模拟测试数据（真实技能）
        test_queries = [
            ("打开空调", "climate_control"),
            ("设置温度", "climate_control"),
            ("座椅加热", "seat_control"),
            ("打开车窗", "window_control"),
            ("播放音乐", "music_media"),
            ("导航到", "navigation"),
            ("打开大灯", "light_control"),
            ("调节音量", "music_media"),
        ]

        # 测试检索
        latencies = []
        category_stats = defaultdict(lambda: {"retrieved": 0, "total": 0})

        for query, true_category in test_queries:
            start = time.perf_counter()
            candidates = retriever.retrieve(query, true_category, top_k=top_k)
            latency = (time.perf_counter() - start) * 1000

            category_stats[true_category]["total"] += 1
            if candidates and candidates[0]['similarity'] > 0.5:
                category_stats[true_category]["retrieved"] += 1

            latencies.append(latency)

        # 计算指标
        latencies = np.array(latencies)

        total_retrieved = sum(s["retrieved"] for s in category_stats.values())
        total_samples = sum(s["total"] for s in category_stats.values())

        accuracy = total_retrieved / total_samples if total_samples > 0 else 0
        precision = accuracy
        recall = accuracy
        f1 = accuracy

        # 每类别统计
        per_category_stats = {}
        for cat, stats in category_stats.items():
            if stats["total"] > 0:
                per_category_stats[cat] = {
                    "accuracy": stats["retrieved"] / stats["total"],
                    "samples": stats["total"]
                }

        result = TestResult(
            stage="技能检索",
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1,
            avg_latency_ms=float(np.mean(latencies)),
            p50_latency_ms=float(np.percentile(latencies, 50)),
            p95_latency_ms=float(np.percentile(latencies, 95)),
            p99_latency_ms=float(np.percentile(latencies, 99)),
            total_samples=total_samples,
            correct_samples=total_retrieved,
            per_category_stats=per_category_stats
        )

        self._print_test_results(result)
        return result

    def test_llm_parser_stage(self) -> TestResult:
        """测试LLM解析阶段"""
        print("\n" + "=" * 70)
        print("阶段3: LLM解析器测试")
        print("=" * 70)

        parser = LLMParser(use_local_llm=False)

        # 测试用例
        test_cases = [
            {
                "input": "打开空调",
                "candidates": [
                    {"skill_id": "OpenAC", "name": "打开空调", "similarity": 0.9}
                ],
                "expected_skill": "OpenAC",
                "expected_params": {"action": "open"}
            },
            {
                "input": "温度24度",
                "candidates": [
                    {"skill_id": "SetTemp", "name": "设置温度", "similarity": 0.8},
                    {"skill_id": "OpenAC", "name": "打开空调", "similarity": 0.5}
                ],
                "expected_skill": "SetTemp",
                "expected_params": {"temperature": 24}
            },
            {
                "input": "座椅加热",
                "candidates": [
                    {"skill_id": "SeatHeat", "name": "座椅加热", "similarity": 0.85}
                ],
                "expected_skill": "SeatHeat",
                "expected_params": {"action": "heat"}
            }
        ]

        # 测试
        latencies = []
        correct = 0

        for case in test_cases:
            start = time.perf_counter()
            result = parser.parse_intent(
                case["input"],
                case["candidates"],
                None
            )
            latency = (time.perf_counter() - start) * 1000
            latencies.append(latency)

            # 检查是否正确
            if result.skill_id == case["expected_skill"]:
                correct += 1

        latencies = np.array(latencies)

        accuracy = correct / len(test_cases)
        result = TestResult(
            stage="LLM解析",
            accuracy=accuracy,
            precision=accuracy,
            recall=accuracy,
            f1=accuracy,
            avg_latency_ms=float(np.mean(latencies)),
            p50_latency_ms=float(np.percentile(latencies, 50)),
            p95_latency_ms=float(np.percentile(latencies, 95)),
            p99_latency_ms=float(np.percentile(latencies, 99)),
            total_samples=len(test_cases),
            correct_samples=correct,
            per_category_stats={}
        )

        self._print_test_results(result)
        return result

    def test_end_to_end(self, num_samples: int = None) -> TestResult:
        """测试端到端推理"""
        print("\n" + "=" * 70)
        print("阶段4: 端到端推理测试")
        print("=" * 70)

        # 初始化推理引擎
        engine = InferenceEngine(
            router_model_path="data/models/router_clean_final/best_model.pth",
            skills_dir=None,
            use_llm=False,
            device=self.device
        )

        if num_samples:
            test_data = self.test_data[:num_samples]
        else:
            test_data = self.test_data

        # 测试
        latencies = []
        category_stats = defaultdict(lambda: {"correct": 0, "total": 0})
        path_stats = defaultdict(int)

        for item in test_data:
            start = time.perf_counter()
            result = engine.process(item["text"], user_id="test")
            latency = (time.perf_counter() - start) * 1000

            latencies.append(latency)

            # 统计类别准确率
            true_category = item.get("category_name", item.get("category", ""))
            if result.category == true_category:
                category_stats[true_category]["correct"] += 1
            category_stats[true_category]["total"] += 1

            # 统计处理路径
            path_stats[result.processing_path.value] += 1

        # 计算指标
        latencies = np.array(latencies)

        total_correct = sum(s["correct"] for s in category_stats.values())
        total_samples = sum(s["total"] for s in category_stats.values())
        accuracy = total_correct / total_samples if total_samples > 0 else 0

        result = TestResult(
            stage="端到端推理",
            accuracy=accuracy,
            precision=accuracy,
            recall=accuracy,
            f1=accuracy,
            avg_latency_ms=float(np.mean(latencies)),
            p50_latency_ms=float(np.percentile(latencies, 50)),
            p95_latency_ms=float(np.percentile(latencies, 95)),
            p99_latency_ms=float(np.percentile(latencies, 99)),
            total_samples=total_samples,
            correct_samples=total_correct,
            per_category_stats={}
        )

        self._print_test_results(result)
        self._print_path_distribution(path_stats)
        return result

    def _print_test_results(self, result: TestResult):
        """打印测试结果"""
        print(f"\n准确率: {result.accuracy*100:.2f}%")
        print(f"精确率: {result.precision*100:.2f}%")
        print(f"召回率: {result.recall*100:.2f}%")
        print(f"F1分数: {result.f1*100:.2f}%")
        print(f"样本数: {result.correct_samples}/{result.total_samples}")

        print(f"\n延迟统计:")
        print(f"  平均: {result.avg_latency_ms:.2f} ms")
        print(f"  P50:  {result.p50_latency_ms:.2f} ms")
        print(f"  P95:  {result.p95_latency_ms:.2f} ms")
        print(f"  P99:  {result.p99_latency_ms:.2f} ms")

        if result.per_category_stats:
            print(f"\n各类别统计:")
            print(f"  {'类别':<20} {'准确率':<10} {'样本数':<8}")
            print("  " + "-" * 40)
            for cat, stats in sorted(result.per_category_stats.items()):
                print(f"  {cat:<20} {stats['accuracy']*100:>8.2f}% {stats['samples']:>8d}")

    def _print_path_distribution(self, path_stats: Dict[str, int]):
        """打印处理路径分布"""
        print(f"\n处理路径分布:")
        for path, count in sorted(path_stats.items(), key=lambda x: x[1], reverse=True):
            pct = count / sum(path_stats.values()) * 100
            print(f"  {path:<20} {count:4d} ({pct:>5.1f}%)")

    def run_all_tests(self, router_samples: int = 100, e2e_samples: int = 50):
        """运行所有测试"""
        results = []

        # 阶段1: 路由分类
        results.append(self.test_router_stage(router_samples))

        # 阶段2: 技能检索
        results.append(self.test_retrieval_stage())

        # 阶段3: LLM解析
        results.append(self.test_llm_parser_stage())

        # 阶段4: 端到端
        results.append(self.test_end_to_end(e2e_samples))

        # 生成总结报告
        self._generate_summary_report(results)

    def _generate_summary_report(self, results: List[TestResult]):
        """生成总结报告"""
        print("\n" + "=" * 70)
        print("性能测试总结报告 (修复版)")
        print("=" * 70)

        print(f"\n{'阶段':<15} {'准确率':<10} {'召回率':<10} {'F1分数':<10} {'平均延迟':<12} {'P95延迟':<12}")
        print("-" * 70)

        for result in results:
            print(f"{result.stage:<15} "
                  f"{result.accuracy*100:>8.2f}% "
                  f"{result.recall*100:>8.2f}% "
                  f"{result.f1*100:>8.2f}% "
                  f"{result.avg_latency_ms:>10.2f} ms "
                  f"{result.p95_latency_ms:>10.2f} ms")

        # 性能目标对比
        print(f"\n性能目标对比:")
        print("-" * 70)

        targets = {
            "路由分类": {"accuracy": 0.95, "p95_latency": 5},
            "技能检索": {"accuracy": 0.80, "p95_latency": 20},
            "LLM解析": {"accuracy": 0.90, "p95_latency": 200},
            "端到端": {"accuracy": 0.90, "p95_latency": 500}
        }

        print(f"{'阶段':<15} {'准确率目标':<12} {'实际':<10} {'P95目标':<10} {'实际P95':<10} {'状态':<8}")
        print("-" * 70)

        all_met = True
        for result in results:
            if result.stage in targets:
                target = targets[result.stage]
                acc_met = result.accuracy >= target["accuracy"]
                lat_met = result.p95_latency_ms <= target["p95_latency"]

                acc_status = "[OK]" if acc_met else "[X]"
                lat_status = "[OK]" if lat_met else "[X]"
                overall_status = "[OK]" if (acc_met and lat_met) else "[X]"

                print(f"{result.stage:<15} "
                      f"{target['accuracy']*100:>10.1f}% "
                      f"{result.accuracy*100:>8.2f}% {acc_status} "
                      f"{target['p95_latency']:>8.0f}ms "
                      f"{result.p95_latency_ms:>8.2f}ms {lat_status} "
                      f"{overall_status}")

                if not (acc_met and lat_met):
                    all_met = False

        print("\n" + "=" * 70)
        if all_met:
            print("[OK] 所有性能指标达标！")
        else:
            print("[!] 部分指标未达标，需要优化")
        print("=" * 70)

        # 关键发现
        print("\n关键发现:")
        print("-" * 70)
        print("1. 路由分类延迟现在是真实的单样本延迟")
        print("2. 端到端延迟 = 路由 + 检索 + LLM解析")
        print("3. Embedding当前使用TF-IDF (CPU)，不支持GPU")
        print("4. 建议: 集成bge-small-zh-v1.5 + FAISS以提升准确率")
        print("=" * 70)


def main():
    """主函数"""
    # 使用清洗后的测试数据
    test_data_path = "data/processed/test_data_clean.json"

    tester = PerformanceTester(test_data_path)

    # 运行所有测试
    tester.run_all_tests(
        router_samples=200,  # 路由测试样本数
        e2e_samples=100       # 端到端测试样本数
    )


if __name__ == "__main__":
    main()
