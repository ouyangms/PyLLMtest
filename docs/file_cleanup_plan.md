# 文件清理计划

## 保留的核心文件

### src/hybrid/ (核心引擎)
- ✅ `architecture.py` - 架构定义
- ✅ `hybrid_retriever.py` - 混合检索器
- ✅ `llm_parser.py` - LLM解析器
- ✅ `skill_executor.py` - 技能执行器
- ✅ `inference_engine_v3.py` - **核心引擎V3**

### src/router/ (路由分类)
- ✅ `textcnn_model.py` - TextCNN模型
- ✅ `category_config.py` - 类别配置
- ✅ `contextual_dialog.py` - 对话路由器
- ✅ `train_router.py` - 训练脚本

### src/data/ (数据处理)
- ✅ `skill_parser.py` - 技能解析
- ✅ `data_processor.py` - 数据处理
- ✅ `query_generator.py` - 查询生成

### src/retrieval/ (向量检索)
- ✅ `embedder.py` - Embedding模型
- ✅ `vector_store.py` - 向量存储
- ✅ `build_index.py` - 索引构建

## 建议删除的文件

### 旧版引擎
- ❌ `src/hybrid/inference_engine.py` - V1引擎（已过时）
- ❌ `src/hybrid/inference_engine_v2.py` - V2引擎（已过时）

### 冗余检索器
- ❌ `src/hybrid/skill_retriever.py` - 原始检索器（已被hybrid_retriever替代）
- ❌ `src/hybrid/skill_retriever_gpu.py` - GPU检索器（已被hybrid_retriever替代）
- ❌ `src/hybrid/skill_retriever_enhanced.py` - 增强检索器（已被hybrid_retriever替代）

### 实验性路由器
- ❌ `src/router/textcnn_enhanced.py` - 增强TextCNN（未使用）
- ❌ `src/router/textcnn_focal.py` - Focal Loss版本（未使用）
- ❌ `src/router/bert_classifier.py` - BERT分类器（测试失败）
- ❌ `src/router/multi_turn_dialog.py` - 旧版多轮对话（已整合）
- ❌ `src/router/classifier.py` - 旧版分类器接口（已过时）

## 清理命令

```bash
# 删除旧版引擎
rm src/hybrid/inference_engine.py
rm src/hybrid/inference_engine_v2.py

# 删除冗余检索器
rm src/hybrid/skill_retriever.py
rm src/hybrid/skill_retriever_gpu.py
rm src/hybrid/skill_retriever_enhanced.py

# 删除实验性路由器
rm src/router/textcnn_enhanced.py
rm src/router/textcnn_focal.py
rm src/router/bert_classifier.py
rm src/router/multi_turn_dialog.py
rm src/router/classifier.py
```

## 清理后的目录结构

```
src/
├── hybrid/
│   ├── architecture.py          # 架构定义
│   ├── hybrid_retriever.py      # 混合检索器
│   ├── llm_parser.py            # LLM解析器
│   ├── skill_executor.py        # 技能执行器
│   └── inference_engine_v3.py   # 核心引擎 V3
│
├── router/
│   ├── textcnn_model.py         # TextCNN 模型
│   ├── category_config.py       # 类别配置
│   ├── contextual_dialog.py     # 对话路由器
│   └── train_router.py          # 训练脚本
│
├── data/
│   ├── skill_parser.py          # 技能解析
│   ├── data_processor.py        # 数据处理
│   └── query_generator.py       # 查询生成
│
└── retrieval/
    ├── embedder.py              # Embedding 模型
    ├── vector_store.py          # 向量存储
    └── build_index.py           # 索引构建
```
