"""
GPU vs CPU 检索器性能测试
使用numpy进行向量检索（避免FAISS GPU依赖问题）
"""

import sys
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')


class SimpleVectorRetriever:
    """简化的向量检索器（使用numpy）"""

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5", device: str = "cpu"):
        """初始化检索器"""
        self.model_name = model_name
        self.device = device
        self.embedder = None
        self.embeddings = {}

        print(f"SimpleVectorRetriever 初始化:")
        print(f"  模型: {model_name}")
        print(f"  设备: {device}")

    def _load_embedder(self):
        """延迟加载embedding模型"""
        if self.embedder is not None:
            return

        try:
            from sentence_transformers import SentenceTransformer
            print(f"加载embedding模型: {self.model_name}")

            self.embedder = SentenceTransformer(
                self.model_name,
                device=self.device
            )

            print(f"  模型设备: {self.embedder.device}")
            print(f"  向量维度: {self.embedder.get_sentence_embedding_dimension()}")

        except ImportError:
            print("错误: sentence-transformers未安装")
            print("安装命令: pip install sentence-transformers")
            raise

    def build_index(self, skills, category: str):
        """为指定类别建立索引"""
        # 延迟加载模型
        self._load_embedder()

        print(f"为 {category} 建立索引 ({len(skills)} 个技能)...")

        # 准备文本
        texts = [skill.get_search_text() for skill in skills]

        # 编码
        start = time.perf_counter()
        embeddings = self.embedder.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        encode_time = (time.perf_counter() - start) * 1000

        print(f"  编码耗时: {encode_time:.2f} ms")
        print(f"  向量维度: {embeddings.shape[1]}")

        # 保存numpy数组
        self.embeddings[category] = {
            'skills': skills,
            'embeddings': embeddings.astype('float32')
        }

    def retrieve(self, query: str, category: str, top_k: int = 3):
        """检索相关技能"""
        if category not in self.embeddings:
            return []

        # 编码查询
        query_embedding = self.embedder.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False
        )

        # 使用numpy计算余弦相似度
        data = self.embeddings[category]
        similarities = np.dot(
            query_embedding,
            data['embeddings'].T
        ).flatten()

        # 获取Top-K
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                results.append((
                    data['skills'][idx],
                    float(similarities[idx])
                ))

        return results


def benchmark_gpu_vs_cpu():
    """GPU vs CPU 性能对比测试"""
    print("=" * 70)
    print("GPU vs CPU 检索器性能对比")
    print("=" * 70)

    # 加载数据
    from src.hybrid.skill_retriever import SkillDatabase, Skill

    skills_dir = Path("E:/ai/py/whisperModel/vc/skills")

    # 创建模拟技能数据库
    print("\n加载技能数据库...")
    db = SkillDatabase()
    db.load_from_directory(skills_dir)

    # 测试查询
    test_queries = [
        ("打开空调", "climate_control"),
        ("座椅加热", "seat_control"),
        ("调节音量", "music_media"),
        ("导航到公司", "navigation"),
        ("打开车窗", "window_control"),
    ]

    batch_sizes = [1, 10, 50, 100]

    print("\n" + "=" * 70)
    print("不同批量大小的性能对比")
    print("=" * 70)

    results = {}

    for batch_size in batch_sizes:
        print(f"\n批次大小: {batch_size}")
        print("-" * 70)

        # CPU测试
        try:
            print("  测试CPU...")
            retriever_cpu = SimpleVectorRetriever(device="cpu")

            # 建立索引（只测试climate_control类别）
            climate_skills = db.get_skills_by_category("climate_control")
            retriever_cpu.build_index(climate_skills, "climate_control")

            # 预热
            for query, _ in test_queries[:3]:
                retriever_cpu.retrieve(query, "climate_control", top_k=3)

            # 正式测试
            latencies_cpu = []
            for _ in range(10):
                start = time.perf_counter()
                for query, category in test_queries[:batch_size]:
                    retriever_cpu.retrieve(query, category, top_k=3)
                latency = (time.perf_counter() - start) * 1000
                latencies_cpu.append(latency)

            avg_cpu = np.mean(latencies_cpu)
            std_cpu = np.std(latencies_cpu)
            print(f"  CPU: {avg_cpu:.2f} ms (std: {std_cpu:.2f} ms)")
            results[f"cpu_{batch_size}"] = avg_cpu

        except Exception as e:
            print(f"  CPU: 错误 - {e}")
            avg_cpu = None

        # GPU测试
        try:
            print("  测试GPU...")
            retriever_gpu = SimpleVectorRetriever(device="cuda")

            # 建立索引
            retriever_gpu.build_index(climate_skills, "climate_control")

            # 预热
            for query, _ in test_queries[:3]:
                retriever_gpu.retrieve(query, "climate_control", top_k=3)

            # 正式测试
            latencies_gpu = []
            for _ in range(10):
                start = time.perf_counter()
                for query, category in test_queries[:batch_size]:
                    retriever_gpu.retrieve(query, category, top_k=3)
                latency = (time.perf_counter() - start) * 1000
                latencies_gpu.append(latency)

            avg_gpu = np.mean(latencies_gpu)
            std_gpu = np.std(latencies_gpu)
            print(f"  GPU: {avg_gpu:.2f} ms (std: {std_gpu:.2f} ms)")
            results[f"gpu_{batch_size}"] = avg_gpu

            if avg_cpu:
                speedup = avg_cpu / avg_gpu
                print(f"  加速比: {speedup:.2f}x")
                if speedup > 1:
                    print(f"  -> GPU快 {speedup:.2f}倍")
                else:
                    print(f"  -> CPU快 {1/speedup:.2f}倍")

        except Exception as e:
            print(f"  GPU: 错误 - {e}")

    # 总结
    print("\n" + "=" * 70)
    print("性能总结")
    print("=" * 70)

    print("\n批次大小 | CPU耗时 | GPU耗时 | 加速比")
    print("-" * 70)

    for batch_size in batch_sizes:
        cpu_time = results.get(f"cpu_{batch_size}", None)
        gpu_time = results.get(f"gpu_{batch_size}", None)

        if cpu_time and gpu_time:
            speedup = cpu_time / gpu_time
            print(f"{batch_size:9d} | {cpu_time:7.2f}ms | {gpu_time:7.2f}ms | {speedup:5.2f}x")
        elif cpu_time:
            print(f"{batch_size:9d} | {cpu_time:7.2f}ms |   N/A   |  N/A ")
        elif gpu_time:
            print(f"{batch_size:9d} |   N/A   | {gpu_time:7.2f}ms |  N/A ")

    print("\n" + "=" * 70)
    print("建议")
    print("=" * 70)

    # 分析建议
    cpu_1 = results.get("cpu_1", None)
    gpu_1 = results.get("gpu_1", None)
    cpu_50 = results.get("cpu_50", None)
    gpu_50 = results.get("gpu_50", None)

    if cpu_1 and gpu_1:
        if cpu_1 < gpu_1:
            print("1. 小批量(<10): 使用CPU，因为传输开销大于计算收益")
        else:
            print("1. 小批量(<10): 使用GPU，仍有加速效果")

    if cpu_50 and gpu_50:
        if gpu_50 < cpu_50:
            print("2. 大批量(>50): 使用GPU，加速效果显著")
        else:
            print("2. 大批量(>50): 使用CPU即可")

    print("3. 推荐配置:")
    print("   - 开发环境: CPU (简单、快速)")
    print("   - 生产环境: GPU (高并发场景)")
    print("=" * 70)


if __name__ == "__main__":
    benchmark_gpu_vs_cpu()
