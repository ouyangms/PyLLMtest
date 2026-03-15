# 技能检索系统 - 实现文档

## 目录
1. [系统概述](#系统概述)
2. [核心组件](#核心组件)
3. [数据加载流程](#数据加载流程)
4. [检索算法详解](#检索算法详解)
5. [性能分析](#性能分析)
6. [优化方案](#优化方案)

---

## 系统概述

技能检索系统是车控语音助手的第二层组件，负责在路由分类确定的类别中，检索出最相关的Top-K技能候选。

### 系统定位

```
用户输入 "打开空调"
    ↓
┌─────────────────────────────┐
│  路由分类器 (TextCNN)        │  → 输出: climate_control (置信度: 0.95)
│  延迟: <1ms                  │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│  技能检索器                  │  → 输出: [OpenAC(0.9), SetTemp(0.5), ...]
│  延迟: <10ms (目标)          │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│  LLM解析器                   │  → 输出: skill_id=OpenAC, params={...}
│  延迟: <300ms                │
└─────────────────────────────┘
```

### 当前状态

| 指标 | 数值 | 目标 | 状态 |
|------|------|------|------|
| 技能总数 | 574个 | 2000+ | ✅ |
| 类别数 | 9个 | 12个 | ⚠️ |
| 检索准确率 | 25% | 80%+ | ❌ |
| 平均延迟 | 0.05ms | <10ms | ✅ |
| 检索方法 | 关键词匹配 | 向量检索 | ⚠️ |

---

## 核心组件

### 1. Skill 数据类

位置: `src/hybrid/skill_retriever.py:19-33`

```python
@dataclass
class Skill:
    """技能定义"""
    skill_id: str           # 唯一标识符
    name: str              # 技能名称
    description: str       # 技能描述
    category: str          # 所属类别
    domain: str            # 所属域 (hvac, body, navigation等)
    params_schema: Dict    # 参数JSON Schema
    example_queries: List[str]  # 示例查询

    def get_search_text(self) -> str:
        """获取用于检索的文本"""
        return f"{self.name} {self.description} {' '.join(self.example_queries)}"
```

**用途**: 统一的技能数据结构，用于存储和检索。

**示例**:
```python
Skill(
    skill_id="OpenAC",
    name="打开空调",
    description="打开空调系统",
    category="climate_control",
    domain="hvac",
    params_schema={"action": "open", "temperature": "integer"},
    example_queries=["打开空调", "开空调", "空调开"]
)
```

---

### 2. SkillDatabase 数据库类

位置: `src/hybrid/skill_retriever.py:35-194`

#### 2.1 数据结构

```python
class SkillDatabase:
    def __init__(self):
        self.skills: List[Skill] = []              # 所有技能列表
        self.skills_by_category: Dict[str, List[Skill]] = {}  # 按类别分组的技能
        self.skill_index: Dict[str, Skill] = {}    # 技能ID索引
```

#### 2.2 数据加载

**加载流程**:
```
1. 读取 vc/skills/skillMetaData.json (列表格式)
   ↓
2. 遍历每个技能元数据
   ↓
3. 推断类别 (_infer_category)
   ↓
4. 提取示例查询 (_extract_examples)
   ↓
5. 创建Skill对象并添加到数据库
   ↓
6. 按类别建立索引 (_index_by_category)
```

**关键代码** (`src/hybrid/skill_retriever.py:43-76`):
```python
def load_from_directory(self, skills_dir: Path):
    """从目录加载技能"""
    metadata_file = skills_dir / "skillMetaData.json"

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)  # 注意: 返回的是列表，不是字典

    for skill_meta in metadata:  # 遍历列表
        skill_name = skill_meta.get("name", "")

        skill = Skill(
            skill_id=skill_meta.get("name", skill_name),
            name=skill_name,
            description=skill_meta.get("description", ""),
            category=self._infer_category(skill_name, skill_meta.get("description", "")),
            domain="vehicle",
            params_schema={},
            example_queries=self._extract_examples(skill_meta.get("description", ""))
        )

        self.skills.append(skill)
        self.skill_index[skill.skill_id] = skill

    self._index_by_category()
```

**⚠️ 重要发现**:
- `skillMetaData.json` 是**列表格式**，不是字典
- 需要遍历列表而不是访问字典键

#### 2.3 类别推断

位置: `src/hybrid/skill_retriever.py:78-106`

使用**关键词匹配**推断类别：

```python
def _infer_category(self, skill_name: str, description: str) -> str:
    """从技能名称和描述推断类别"""
    text = (skill_name + " " + description).lower()

    # 基于关键词推断类别
    if any(kw in text for kw in ["air conditioner", "temperature", "ac", "climate", "空调", "温度"]):
        return "climate_control"
    elif any(kw in text for kw in ["seat", "heating", "ventilation", "massage", "座椅", "加热", "通风"]):
        return "seat_control"
    # ... 其他类别
    else:
        return "system_settings"
```

**支持的关键词映射**:

| 类别 | 关键词（中文/英文） |
|------|---------------------|
| climate_control | 空调/温度/AC/air conditioner/temperature |
| seat_control | 座椅/加热/通风/seat/heating/ventilation |
| window_control | 车窗/天窗/遮阳/window/sunroof/shade |
| light_control | 灯光/灯/light/lamp/beam |
| mirror_control | 镜子/后视镜/mirror |
| door_control | 车门/后备箱/锁/door/trunk/lock |
| music_media | 音乐/音量/music/audio/volume |
| navigation | 导航/路线/GPS/navigation/route |
| phone_call | 电话/拨打/phone/call |
| charging_energy | 电量/充电/续航/battery/charging |
| driving_assist | 巡航/车道/辅助/cruise/lane/assist |
| system_settings | 默认类别 |

**⚠️ 问题**:
- 简单的关键词匹配容易误判
- 无法处理同义词和变体
- 例如："关闭后排座椅加热" 可能被误判为 climate_control

#### 2.4 示例查询提取

位置: `src/hybrid/skill_retriever.py:108-116`

使用**正则表达式**提取括号中的内容：

```python
def _extract_examples(self, description: str) -> List[str]:
    """从描述中提取示例查询"""
    examples = []
    # 提取括号中的中文内容
    import re
    pattern = r'\(([^\)]+)\)'  # 匹配括号内容
    matches = re.findall(pattern, description)
    examples.extend(matches)
    return examples[:3]  # 最多3个示例
```

**示例**:
- 输入: `"打开空调（打开空调系统，自动模式）"`
- 输出: `["打开空调系统，自动模式"]`

**⚠️ 问题**:
- 提取规则过于简单
- 无法处理多样化的描述格式
- 示例数量有限（最多3个）

---

### 3. VectorRetriever 向量检索类

位置: `src/hybrid/skill_retriever.py:196-259`

#### 3.1 当前实现

使用 **TF-IDF + 余弦相似度** 作为向量检索的占位实现：

```python
class VectorRetriever:
    def __init__(self, use_faiss: bool = False):
        self.use_faiss = use_faiss  # 当前未使用FAISS
        self.embeddings = {}
        self.faiss_index = None

    def build_index(self, skills: List[Skill], category: str):
        """为指定类别建立索引"""
        # 使用TF-IDF作为占位符
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        texts = [skill.get_search_text() for skill in category_skills]

        # 创建TF-IDF向量
        self.vectorizer = TfidfVectorizer(max_features=100)
        tfidf_matrix = self.vectorizer.fit_transform(texts)

        self.embeddings[category] = {
            'skills': category_skills,
            'matrix': tfidf_matrix,
            'vectorizer': self.vectorizer
        }
```

**⚠️ 问题**:
- TF-IDF是传统方法，无法理解语义
- max_features=100 特征数量太少
- 没有集成真正的embedding模型（如bge-small-zh-v1.5）

#### 3.2 检索方法

```python
def retrieve(self, query: str, category: str, top_k: int = 3):
    """检索相关技能"""
    data = self.embeddings[category]
    query_vec = data['vectorizer'].transform([query])
    similarities = cosine_similarity(query_vec, data['matrix']).flatten()

    # 获取Top-K
    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []
    for idx in top_indices:
        if similarities[idx] > 0:
            results.append((data['skills'][idx], float(similarities[idx])))

    return results
```

---

### 4. SkillRetriever 主接口

位置: `src/hybrid/skill_retriever.py:262-327`

#### 4.1 初始化

```python
class SkillRetriever:
    def __init__(self, skills_dir: Path, use_vector: bool = False):
        self.db = SkillDatabase()
        self.db.load_from_directory(skills_dir)

        self.vector_retriever = None
        if use_vector:
            self.vector_retriever = VectorRetriever(use_faiss=False)
            self._build_vector_indices()
```

**参数说明**:
- `skills_dir`: 技能目录路径 (如 `vc/skills/`)
- `use_vector`: 是否使用向量检索（默认False，使用关键词检索）

#### 4.2 检索接口

```python
def retrieve(
    self,
    query: str,         # 用户查询
    category: str,      # 路由分类结果
    top_k: int = 3,     # 返回Top-K结果
    method: str = "hybrid"  # 检索方法 (keyword/vector/hybrid)
) -> List[Dict]:
    """
    检索技能

    Returns:
        [
            {
                'skill_id': 'OpenAC',
                'name': '打开空调',
                'description': '打开空调系统',
                'params_schema': {...},
                'similarity': 0.9,
                'category': 'climate_control'
            },
            ...
        ]
    """
```

---

## 检索算法详解

### 1. 关键词检索 (默认)

位置: `src/hybrid/skill_retriever.py:134-168`

#### 1.1 算法流程

```
输入: query="打开空调", category="climate_control"
    ↓
1. 确定搜索范围 (该类别的所有技能)
    ↓
2. 对每个技能计算相似度分数
    ↓
3. 按分数排序
    ↓
4. 返回Top-K结果
```

#### 1.2 相似度计算

位置: `src/hybrid/skill_retriever.py:169-189`

```python
def _calculate_similarity(self, query: str, skill: Skill) -> float:
    """计算查询与技能的相似度"""
    score = 0.0

    # 1. 名称完全匹配
    if query in skill.name.lower():
        score += 1.0

    # 2. 描述包含查询
    if query in skill.description.lower():
        score += 0.5

    # 3. 示例查询完全匹配
    for example in skill.example_queries:
        if query in example.lower():
            score += 0.3
        # 部分匹配
        elif any(word in example.lower() for word in query.split()):
            score += 0.1

    return score
```

**评分规则**:

| 匹配类型 | 分数 | 说明 |
|---------|------|------|
| 名称完全匹配 | +1.0 | 查询是技能名称的子串 |
| 描述包含查询 | +0.5 | 描述包含查询文本 |
| 示例完全匹配 | +0.3 | 查询匹配某个示例 |
| 示例部分匹配 | +0.1 | 查询的某个词在示例中 |

#### 1.3 示例

查询: `"打开空调"`, 类别: `climate_control`

| 技能 | 计算过程 | 总分 |
|------|----------|------|
| 打开空调 | 名称匹配: +1.0, 示例匹配: +0.3 | 1.3 |
| 设置空调温度 | 描述包含: +0.5 | 0.5 |
| 座椅加热 | 无匹配 | 0.0 |

**结果排序**: 打开空调(1.3) > 设置空调温度(0.5)

**⚠️ 问题**:
- 无法理解语义相似性
- "打开空调" 和 "开一下空调" 分数不同
- "太热了" 无法匹配到"打开空调"

---

### 2. 向量检索 (可选)

位置: `src/hybrid/skill_retriever.py:234-259`

#### 2.1 算法流程

```
输入: query="打开空调", category="climate_control"
    ↓
1. 使用TfidfVectorizer将查询转换为向量
    ↓
2. 计算查询向量与所有技能向量的余弦相似度
    ↓
3. 返回相似度最高的Top-K个技能
```

#### 2.2 公式

**余弦相似度**:
```
similarity(query, skill) = (query · skill) / (||query|| × ||skill||)
```

其中:
- `query`: 查询的TF-IDF向量
- `skill`: 技能的TF-IDF向量
- `||·||`: 向量的L2范数

**⚠️ 问题**:
- TF-IDF无法捕获语义信息
- 需要使用真正的embedding模型（如bge-small-zh-v1.5）

---

### 3. 混合检索 (推荐)

结合关键词和向量检索的优势：

```python
def retrieve_hybrid(self, query: str, category: str, top_k: int = 3):
    """混合检索"""
    # 1. 关键词检索 (快速过滤)
    keyword_results = self.db.search_by_keywords(query, category, top_k=10)

    # 2. 向量检索 (语义匹配)
    vector_results = self.vector_retriever.retrieve(query, category, top_k=10)

    # 3. 融合分数
    combined_scores = {}
    for skill, score in keyword_results:
        combined_scores[skill.skill_id] = score * 0.6  # 关键词权重60%

    for skill, score in vector_results:
        if skill.skill_id in combined_scores:
            combined_scores[skill.skill_id] += score * 0.4  # 向量权重40%
        else:
            combined_scores[skill.skill_id] = score * 0.4

    # 4. 排序并返回Top-K
    results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    return results[:top_k]
```

---

## 性能分析

### 当前性能 (基于性能测试报告)

| 指标 | 数值 | 目标 | 状态 |
|------|------|------|------|
| **准确率** | 25.00% | 80%+ | ❌ |
| **平均延迟** | 0.05 ms | <10 ms | ✅ |
| **P95延迟** | 0.12 ms | <20 ms | ✅ |
| **P99延迟** | 0.13 ms | <50 ms | ✅ |

### 各类别准确率

| 类别 | 准确率 | 样本数 | 状态 |
|------|--------|--------|------|
| seat_control | 100.00% | 1 | ✅ |
| climate_control | 50.00% | 2 | ⚠️ |
| light_control | 0.00% | 1 | ❌ |
| music_media | 0.00% | 2 | ❌ |
| navigation | 0.00% | 1 | ❌ |
| window_control | 0.00% | 1 | ❌ |

### 问题分析

#### 1. 为什么准确率只有25%?

**原因1: 简单的字符串匹配**
- 当前算法只检查子串匹配
- 无法理解语义相似性
- 例如: "调大音量" 无法匹配到 "调节音量"

**原因2: 示例查询不足**
- 每个技能最多3个示例
- 示例提取规则过于简单
- 缺少同义词和口语表达

**原因3: 类别推断错误**
- 基于关键词的推断容易误判
- 例如: "关闭后排座椅加热" 可能被推断为 climate_control

#### 2. 为什么延迟这么低?

**原因**:
- 没有使用深度学习模型
- 纯粹的字符串操作
- 没有embedding计算

**代价**: 牺牲了准确率

---

## 优化方案

### 方案1: 集成真正的向量检索 (推荐)

#### 1.1 使用 bge-small-zh-v1.5 Embedding模型

```python
from sentence_transformers import SentenceTransformer

class VectorRetriever:
    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        self.embedder = SentenceTransformer(model_name)
        self.embeddings = {}

    def build_index(self, skills: List[Skill], category: str):
        """为指定类别建立向量索引"""
        category_skills = [s for s in skills if s.category == category]

        # 使用bge-small-zh-v1.5编码
        texts = [skill.get_search_text() for skill in category_skills]
        embeddings = self.embedder.encode(texts, normalize_embeddings=True)

        # 使用FAISS建立索引
        import faiss
        index = faiss.IndexFlatIP(embeddings.shape[1])  # 内积索引
        index.add(embeddings.astype('float32'))

        self.embeddings[category] = {
            'skills': category_skills,
            'index': index,
            'embeddings': embeddings
        }
```

**优势**:
- 真正的语义理解
- 支持同义词匹配
- 准确率预计提升到70%+

#### 1.2 使用FAISS加速检索

```python
import faiss
import numpy as np

class VectorRetriever:
    def retrieve(self, query: str, category: str, top_k: int = 3):
        """使用FAISS检索"""
        data = self.embeddings[category]

        # 编码查询
        query_embedding = self.embedder.encode(
            [query],
            normalize_embeddings=True
        )

        # FAISS检索
        scores, indices = data['index'].search(
            query_embedding.astype('float32'),
            top_k
        )

        # 返回结果
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                results.append((
                    data['skills'][idx],
                    float(score)
                ))

        return results
```

**性能**:
- 单次检索: <5ms (CPU)
- 单次检索: <1ms (GPU)

---

### 方案2: 改进关键词检索

#### 2.1 添加同义词匹配

```python
SYNONYMS = {
    "打开": ["开启", "开", "启动"],
    "关闭": ["关", "关闭", "停止"],
    "空调": ["ac", "air conditioner"],
    "音量": ["声音", "音效"],
    # ...
}

def _calculate_similarity(self, query: str, skill: Skill) -> float:
    """改进的相似度计算"""
    score = 0.0

    # 1. 直接匹配
    if query in skill.name.lower():
        score += 1.0

    # 2. 同义词匹配
    for word, synonyms in SYNONYMS.items():
        if word in query:
            for synonym in synonyms:
                if synonym in skill.name.lower():
                    score += 0.8

    # 3. 分词匹配
    query_words = set(query.split())
    skill_words = set(skill.get_search_text().split())
    overlap = len(query_words & skill_words) / len(query_words)
    score += overlap * 0.5

    return score
```

#### 2.2 使用jieba分词

```python
import jieba

def _calculate_similarity(self, query: str, skill: Skill) -> float:
    """使用分词的相似度计算"""
    score = 0.0

    # 分词
    query_words = set(jieba.lcut(query))
    skill_words = set(jieba.lcut(skill.get_search_text()))

    # 计算Jaccard相似度
    intersection = len(query_words & skill_words)
    union = len(query_words | skill_words)
    jaccard = intersection / union if union > 0 else 0

    score = jaccard * 2.0  # 放大分数

    return score
```

---

### 方案3: 数据增强

#### 3.1 自动生成更多示例查询

```python
def generate_examples(skill: Skill, num_examples: int = 10) -> List[str]:
    """为技能生成更多示例查询"""

    templates = [
        # 标准指令型
        f"{skill.name}",
        f"请{skill.name}",
        f"帮我{skill.name}",

        # 场景/感受型
        f"现在太热了",  # 假设是空调技能
        f"感觉有点冷",

        # 模糊/口语型
        f"调一下{skill.name.split()[0]}",
        f"弄一下{skill.name.split()[0]}",

        # 否定/反向型
        f"不要{skill.name}",
        f"取消{skill.name.split()[0]}",

        # 组合/上下文型
        f"把{skill.name.split()[0]}调到最大",
        f"我想{skill.name.split()[0]}",
    ]

    return templates[:num_examples]
```

#### 3.2 使用LLM生成样本

参考 `scripts/llm_augment_qwen.py` 的实现，为每个技能生成8-10个多样化的示例查询。

---

### 方案4: 混合检索策略

```python
def retrieve_hybrid(
    self,
    query: str,
    category: str,
    top_k: int = 3,
    keyword_weight: float = 0.3,
    vector_weight: float = 0.7
) -> List[Dict]:
    """混合检索：结合关键词和向量"""

    # 1. 关键词检索 (召回)
    keyword_results = self.db.search_by_keywords(query, category, top_k=20)

    # 2. 向量检索 (精排)
    vector_results = self.vector_retriever.retrieve(query, category, top_k=20)

    # 3. 融合分数
    combined = {}
    for skill, score in keyword_results:
        combined[skill.skill_id] = {
            'skill': skill,
            'score': score * keyword_weight,
            'keyword_score': score
        }

    for skill, score in vector_results:
        if skill.skill_id in combined:
            combined[skill.skill_id]['score'] += score * vector_weight
            combined[skill.skill_id]['vector_score'] = score
        else:
            combined[skill.skill_id] = {
                'skill': skill,
                'score': score * vector_weight,
                'vector_score': score
            }

    # 4. 排序并返回Top-K
    results = sorted(combined.items(), key=lambda x: x[1]['score'], reverse=True)

    return [
        {
            'skill_id': item['skill'].skill_id,
            'name': item['skill'].name,
            'similarity': item['score'],
            'keyword_score': item.get('keyword_score', 0),
            'vector_score': item.get('vector_score', 0),
        }
        for skill_id, item in results[:top_k]
    ]
```

---

## 实施建议

### 短期 (1周内)

1. ✅ **改进示例查询提取**
   - 优化正则表达式规则
   - 增加示例数量限制（5-10个）

2. ✅ **添加同义词匹配**
   - 创建同义词词典
   - 改进相似度计算

3. ✅ **使用jieba分词**
   - 改进中文分词
   - 提升匹配准确率

**预期效果**: 准确率从25%提升到40-50%

---

### 中期 (2-4周)

1. ⚠️ **集成bge-small-zh-v1.5**
   - 实现真正的向量检索
   - 使用FAISS加速

2. ⚠️ **实现混合检索**
   - 结合关键词和向量
   - 优化权重参数

3. ⚠️ **数据增强**
   - 使用LLM生成更多示例
   - 确保每个技能≥8条示例

**预期效果**: 准确率提升到70-80%

---

### 长期 (1-2月)

1. 🔄 **端到端优化**
   - 联合训练路由和检索
   - 优化整个推理流程

2. 🔄 **个性化检索**
   - 基于用户历史调整
   - 上下文感知检索

3. 🔄 **持续学习**
   - 在线学习用户反馈
   - 自动更新检索模型

**预期效果**: 准确率提升到85-90%

---

## 总结

### 当前状态
- ✅ 已实现基础的关键词检索
- ✅ 加载574个技能
- ✅ 支持9个类别
- ❌ 检索准确率仅25%
- ✅ 延迟0.05ms（远超目标）

### 核心问题
1. 简单的字符串匹配无法理解语义
2. 示例查询不足且提取规则简单
3. 缺少真正的向量检索实现

### 优化方向
1. **短期**: 改进关键词匹配，添加同义词和分词
2. **中期**: 集成bge-small-zh-v1.5和FAISS，实现真正的向量检索
3. **长期**: 端到端优化和个性化检索

### 预期效果
| 阶段 | 准确率 | 延迟 | 说明 |
|------|--------|------|------|
| 当前 | 25% | 0.05ms | 关键词匹配 |
| 短期 | 40-50% | <1ms | 改进关键词 |
| 中期 | 70-80% | <5ms | 向量检索 |
| 长期 | 85-90% | <10ms | 端到端优化 |

---

**文档版本**: v1.0
**创建日期**: 2024年
**最后更新**: 2024年
**状态**: ✅ 完成
