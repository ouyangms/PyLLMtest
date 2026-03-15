"""
混合检索器 - 结合关键词和向量检索
目标：准确率 >80%, 延迟 <10ms
"""

import json
import sys
import time
import pickle
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import numpy as np

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.router.category_config import CategoryConfig


@dataclass
class Skill:
    """技能定义"""
    skill_id: str
    name: str
    description: str
    category: str
    domain: str
    params_schema: Dict
    example_queries: List[str]

    def get_search_text(self) -> str:
        """获取用于检索的文本"""
        return f"{self.name} {self.description} {' '.join(self.example_queries)}"


class HybridRetriever:
    """混合检索器：关键词 + 向量"""

    def __init__(
        self,
        skills_dir: Path,
        use_embedding: bool = True,
        model_name: str = "BAAI/bge-small-zh-v1.5",
        device: str = "auto"
    ):
        """
        初始化混合检索器

        Args:
            skills_dir: 技能目录
            use_embedding: 是否使用向量检索
            model_name: embedding模型名称
            device: 设备 (auto/cpu/cuda)
        """
        self.skills_dir = skills_dir
        self.use_embedding = use_embedding
        self.model_name = model_name
        self.device = self._determine_device(device)

        # 技能数据库
        self.skills: List[Skill] = []
        self.skills_by_category: Dict[str, List[Skill]] = {}
        self.skill_index: Dict[str, Skill] = {}

        # 关键词检索组件
        self.synonyms = self._load_synonyms()

        # 向量检索组件
        self.embedder = None
        self.embeddings: Dict[str, np.ndarray] = {}  # category -> embeddings

        # 加载技能
        self._load_skills()

        # 如果需要，建立向量索引
        if self.use_embedding:
            self._build_embedding_index()

    def _determine_device(self, device: str) -> str:
        """确定使用的设备"""
        if device != "auto":
            return device

        try:
            import torch
            if torch.cuda.is_available():
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                if gpu_memory >= 2:
                    return "cuda"
        except:
            pass

        return "cpu"

    def _load_synonyms(self) -> Dict[str, List[str]]:
        """加载同义词词典"""
        return {
            "打开": ["开启", "开", "启动"],
            "关闭": ["关", "停止", "熄灭"],
            "空调": ["ac", "冷气"],
            "座椅": ["座位", "椅子"],
            "车窗": ["窗户", "玻璃"],
            "音量": ["声音", "音效"],
            "导航": ["GPS", "路线"],
            "电话": ["呼叫", "拨打"],
            # ... 更多同义词
        }

    def _load_skills(self):
        """加载技能"""
        print(f"从 {self.skills_dir} 加载技能...")

        metadata_file = self.skills_dir / "skillMetaData.json"
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            print(f"找到 {len(metadata)} 个技能元数据")

            for skill_meta in metadata:
                skill_name = skill_meta.get("name", "")

                skill = Skill(
                    skill_id=skill_meta.get("name", skill_name),
                    name=skill_meta.get("name", skill_name),
                    description=skill_meta.get("description", ""),
                    category=self._infer_category(skill_name, skill_meta.get("description", "")),
                    domain="vehicle",
                    params_schema={},
                    example_queries=self._extract_examples(skill_meta.get("description", ""))
                )

                self.skills.append(skill)
                self.skill_index[skill.skill_id] = skill

        print(f"成功加载 {len(self.skills)} 个技能")
        self._index_by_category()

    def _infer_category(self, skill_name: str, description: str) -> str:
        """从技能名称和描述推断类别"""
        text = (skill_name + " " + description).lower()

        if any(kw in text for kw in ["空调", "温度", "ac", "climate"]):
            return "climate_control"
        elif any(kw in text for kw in ["座椅", "seat", "加热", "通风"]):
            return "seat_control"
        elif any(kw in text for kw in ["车窗", "window", "天窗", "sunroof"]):
            return "window_control"
        elif any(kw in text for kw in ["灯光", "灯", "light"]):
            return "light_control"
        elif any(kw in text for kw in ["音乐", "music", "音量", "volume"]):
            return "music_media"
        elif any(kw in text for kw in ["导航", "navigation", "gps"]):
            return "navigation"
        elif any(kw in text for kw in ["电话", "phone", "拨打"]):
            return "phone_call"
        elif any(kw in text for kw in ["镜子", "mirror", "后视镜"]):
            return "mirror_control"
        elif any(kw in text for kw in ["车门", "door", "后备箱", "trunk", "锁"]):
            return "door_control"
        else:
            return "system_settings"

    def _extract_examples(self, description: str) -> List[str]:
        """从描述中提取示例查询"""
        examples = []
        import re
        pattern = r'\(([^\)]+)\)'
        matches = re.findall(pattern, description)
        examples.extend(matches)

        # 如果示例不足，添加一些默认的
        if len(examples) < 2:
            skill_lower = description.lower()
            if "打开" in skill_lower or "开启" in skill_lower:
                examples.append("打开")
            if "关闭" in skill_lower:
                examples.append("关闭")
            if "调节" in skill_lower or "调整" in skill_lower:
                examples.append("调节")

        return examples[:5]

    def _index_by_category(self):
        """按类别建立索引"""
        self.skills_by_category = {}
        for skill in self.skills:
            if skill.category not in self.skills_by_category:
                self.skills_by_category[skill.category] = []
            self.skills_by_category[skill.category].append(skill)

        print(f"\n技能类别分布:")
        for category, skills in sorted(self.skills_by_category.items()):
            print(f"  {category}: {len(skills)} 个技能")

    def _load_embedder(self):
        """延迟加载embedding模型"""
        if self.embedder is not None:
            return

        try:
            from sentence_transformers import SentenceTransformer
            print(f"\n加载embedding模型: {self.model_name}")

            self.embedder = SentenceTransformer(
                self.model_name,
                device=self.device
            )

            print(f"  模型设备: {self.embedder.device}")
            print(f"  向量维度: {self.embedder.get_sentence_embedding_dimension()}")

        except ImportError:
            print("警告: sentence-transformers未安装")
            print("安装命令: pip install sentence-transformers")
            raise

    def _build_embedding_index(self):
        """建立向量索引"""
        self._load_embedder()

        print("\n建立向量索引...")
        for category, skills in self.skills_by_category.items():
            if len(skills) == 0:
                continue

            print(f"  为 {category} 编码 ({len(skills)} 个技能)...")

            # 准备文本
            texts = [skill.get_search_text() for skill in skills]

            # 编码
            embeddings = self.embedder.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
                convert_to_numpy=True
            )

            # 保存
            self.embeddings[category] = embeddings.astype('float32')

        print("  向量索引建立完成")

    def retrieve(
        self,
        query: str,
        category: str,
        top_k: int = 3,
        keyword_weight: float = 0.4,
        vector_weight: float = 0.6
    ) -> List[Dict]:
        """
        混合检索

        Args:
            query: 用户查询
            category: 类别
            top_k: 返回Top-K结果
            keyword_weight: 关键词检索权重
            vector_weight: 向量检索权重

        Returns:
            技能候选列表
        """
        # 1. 关键词检索
        keyword_results = self._keyword_search(query, category, top_k * 2)

        # 2. 向量检索
        if self.use_embedding and category in self.embeddings:
            vector_results = self._vector_search(query, category, top_k * 2)
        else:
            vector_results = []

        # 3. 融合结果
        combined = self._merge_results(
            keyword_results,
            vector_results,
            keyword_weight,
            vector_weight
        )

        # 4. 排序并返回Top-K
        combined.sort(key=lambda x: x['similarity'], reverse=True)
        return combined[:top_k]

    def _keyword_search(
        self,
        query: str,
        category: str,
        top_k: int
    ) -> List[Tuple[Skill, float]]:
        """关键词搜索"""
        category_skills = self.skills_by_category.get(category, [])
        query_lower = query.lower()

        results = []
        for skill in category_skills:
            score = 0.0

            # 完全匹配
            if query_lower in skill.name.lower():
                score += 2.0

            if query_lower in skill.description.lower():
                score += 1.0

            # 示例匹配
            for example in skill.example_queries:
                if query_lower in example.lower():
                    score += 0.5

            # 同义词匹配
            for word, synonyms in self.synonyms.items():
                if word in query_lower:
                    for synonym in synonyms:
                        if synonym in skill.name.lower():
                            score += 0.3

            if score > 0:
                results.append((skill, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _vector_search(
        self,
        query: str,
        category: str,
        top_k: int
    ) -> List[Tuple[Skill, float]]:
        """向量搜索"""
        if category not in self.embeddings:
            return []

        # 编码查询
        query_embedding = self.embedder.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False
        )

        # 计算相似度
        category_skills = self.skills_by_category[category]
        embeddings = self.embeddings[category]

        similarities = np.dot(query_embedding, embeddings.T).flatten()

        # 获取Top-K
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                results.append((
                    category_skills[idx],
                    float(similarities[idx])
                ))

        return results

    def _merge_results(
        self,
        keyword_results: List[Tuple[Skill, float]],
        vector_results: List[Tuple[Skill, float]],
        keyword_weight: float,
        vector_weight: float
    ) -> List[Dict]:
        """融合关键词和向量检索结果"""
        combined = {}

        # 添加关键词结果
        for skill, score in keyword_results:
            combined[skill.skill_id] = {
                'skill': skill,
                'keyword_score': score,
                'vector_score': 0.0,
                'similarity': score * keyword_weight
            }

        # 添加向量结果
        for skill, score in vector_results:
            if skill.skill_id in combined:
                combined[skill.skill_id]['vector_score'] = score
                combined[skill.skill_id]['similarity'] += score * vector_weight
            else:
                combined[skill.skill_id] = {
                    'skill': skill,
                    'keyword_score': 0.0,
                    'vector_score': score,
                    'similarity': score * vector_weight
                }

        # 转换为列表
        results = []
        for skill_id, data in combined.items():
            skill = data['skill']
            results.append({
                'skill_id': skill.skill_id,
                'name': skill.name,
                'description': skill.description,
                'params_schema': skill.params_schema,
                'similarity': data['similarity'],
                'keyword_score': data['keyword_score'],
                'vector_score': data['vector_score'],
                'category': skill.category
            })

        return results

    def get_all_skills_count(self) -> int:
        """获取技能总数"""
        return len(self.skills)

    def get_categories(self) -> List[str]:
        """获取所有类别"""
        return list(self.skills_by_category.keys())


if __name__ == "__main__":
    # 测试混合检索器
    print("=" * 70)
    print("混合检索器测试")
    print("=" * 70)

    skills_dir = Path("E:/ai/py/whisperModel/vc/skills")

    # 初始化
    retriever = HybridRetriever(
        skills_dir,
        use_embedding=True,
        device="cuda"
    )

    # 测试查询
    test_queries = [
        ("打开空调", "climate_control"),
        ("座椅加热", "seat_control"),
        ("调大音量", "music_media"),
        ("导航到公司", "navigation"),
    ]

    print("\n" + "=" * 70)
    print("测试检索")
    print("=" * 70)

    for query, category in test_queries:
        print(f"\n查询: \"{query}\" (类别: {category})")

        start = time.perf_counter()
        candidates = retriever.retrieve(query, category, top_k=3)
        latency = (time.perf_counter() - start) * 1000

        if candidates:
            for i, candidate in enumerate(candidates, 1):
                print(f"  {i}. {candidate['name']}")
                print(f"     相似度: {candidate['similarity']:.2f} "
                      f"(关键词: {candidate['keyword_score']:.2f}, "
                      f"向量: {candidate['vector_score']:.2f})")
        else:
            print("  未找到相关技能")

        print(f"  延迟: {latency:.2f} ms")
