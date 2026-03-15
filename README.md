# 车控技能推理引擎

针对高通 8295 平台的车控语音助手系统，支持 2000+ 车控技能的离线部署。

## 系统架构

### 三级推理架构

1. **路由层** - TextCNN 分类器，延迟 <10ms
2. **检索层** - FAISS 向量检索，延迟 <50ms
3. **生成层** - LLM 决策（待集成）

## 项目结构

```
whisperModel/
├── src/                          # 源代码
│   ├── data/                     # 数据处理
│   │   ├── skill_parser.py       # 技能解析器
│   │   ├── query_generator.py    # LLM 样本生成器
│   │   └── data_processor.py     # 数据处理器
│   ├── router/                   # 路由分类
│   │   ├── category_config.py    # 分类配置
│   │   ├── textcnn_model.py      # TextCNN 模型
│   │   ├── train_router.py       # 训练脚本
│   │   └── classifier.py         # 推理接口
│   └── retrieval/                # 向量检索
│       ├── embedder.py           # 嵌入模型
│       ├── build_index.py        # 索引构建
│       └── vector_store.py       # 向量存储
├── scripts/                      # 执行脚本
│   ├── setup_env.py              # 环境设置
│   ├── parse_skills.py           # 解析技能
│   ├── generate_queries.py       # 生成样本
│   ├── process_data.py           # 处理数据
│   ├── train_router.py           # 训练模型
│   └── build_indexes.py          # 构建索引
├── vc/skills/                    # 技能定义 (575个)
├── data/                         # 数据目录
│   ├── processed/                # 处理后的数据
│   ├── models/                   # 模型文件
│   └── indexes/                  # 向量索引
└── requirements.txt              # 依赖项
```

## 快速开始

### 1. 环境设置

```bash
# 自动安装依赖
python scripts/setup_env.py

# 或手动安装
pip install -r requirements.txt
```

### 2. 数据处理

```bash
# 解析技能文件
python scripts/parse_skills.py

# 生成训练样本 (可选: 使用 --with-api 启用 LLM 生成)
python scripts/generate_queries.py

# 处理训练数据
python scripts/process_data.py
```

### 3. 模型训练

```bash
# 训练路由分类器
python scripts/train_router.py
```

### 4. 向量索引

```bash
# 构建 FAISS 索引
python scripts/build_indexes.py
```

## 技术规格

| 组件 | 模型 | 大小 | 延迟 |
|------|------|------|------|
| 路由模型 | TextCNN | <5MB | <10ms |
| 嵌入模型 | bge-small-zh | ~30MB | - |
| 检索引擎 | FAISS | - | <50ms |

## 分类体系

13 个主要分类:
- climate_control (空调控制)
- seat_control (座椅控制)
- window_control (车窗控制)
- light_control (灯光控制)
- mirror_control (后视镜控制)
- door_control (车门控制)
- music_media (音乐媒体)
- navigation (导航)
- phone_call (电话)
- vehicle_info (车辆信息)
- system_settings (系统设置)
- driving_assist (驾驶辅助)
- charging_energy (充电/能源)

## 验证标准

- 准确率: Top-1 >90%
- 延迟: P99 <1000ms
- 资源: 内存 <3GB

## 下一步

- [ ] 集成 Gemma 3 LLM
- [ ] 实现端到端推理
- [ ] 模型量化和 ONNX 导出
- [ ] 端侧性能优化
