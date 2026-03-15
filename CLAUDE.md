# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个针对高通 8295 平台的车控语音助手系统设计项目，目标是实现 **2000+ 车控技能**的离线部署，要求延迟 <1s 且准确率 >95%。

## 系统架构

本项目采用**三级架构**设计：

### 1. 路由层 (Router Layer)
- 使用轻量级文本分类模型 (TextCNN 或 DistilBERT)
- 将用户指令路由到正确的技能类别 (如 climate_control, window_control)
- 模型量化为 INT8，转换为 ONNX/TFLite 格式
- 目标延迟: < 20ms

### 2. 检索层 (Retrieval Layer)
- 基于 FAISS 或 ScaNN 的向量检索
- 按 category 建立 10-20 个独立索引文件 (而非单一大型索引)
- 使用 bge-small-zh-v1.5 或 all-MiniLM-L6-v2 作为 Embedding 模型
- 每个 category 检索 Top-3 候选技能
- 目标延迟: < 50ms

### 3. 生成层 (Generation Layer)
- 使用 Gemma 3n E2B (量化为 Q4_K_M)
- 通过 llama.cpp 部署，支持 Vulkan GPU 加速或 QNN NPU
- 使用 Grammar Constrained Decoding (gbnf) 强制输出 JSON 格式
- 目标延迟: < 300ms

## 核心数据结构

### 技能定义 (Skills Database)
每个技能包含以下字段：
- `skill_id`: 唯一标识符
- `category`: 技能分类 (用于路由)
- `domain`: 所属域 (hvac, body, etc.)
- `description`: 技能描述
- `params_schema`: 参数 JSON Schema
- `example_queries`: 典型用户问法列表
- `execution_code`: 执行代码

## 推理流程

系统按以下顺序处理用户指令：

1. **规则匹配**: 极速拦截常见指令
2. **意图路由**: Router 分类器预测 category
3. **向量检索**: 在对应 category 的子索引中搜索候选技能
4. **LLM 决策**: 从候选技能中选择并提取参数
5. **执行**: 调用对应的执行代码

## 关键优化技术

- **按 Category 分片索引**: 显著提升检索速度
- **Grammar Constrained Decoding**: 确保输出格式正确，减少幻觉
- **Context Caching**: 缓存 System Prompt 和车辆状态，降低 TTFT
- **并行流水线**: ASR 流式输出时预触发 Router 预测

## 开发环境

- **目标平台**: 高通 8295 (Android Automotive OS / Linux)
- **SDK**: Qualcomm AI Engine Direct (QNN)
- **推理框架**:
  - LLM: llama.cpp
  - Router/Embedding: ONNX Runtime + QNN Execution Provider
- **检索库**: FAISS 或 ScaNN

## 测试标准

- **准确率**: Top-1 技能匹配率 > 95%
- **延迟**: P99 < 1000ms, P95 < 800ms
- **资源占用**: 内存 < 3GB, NPU 利用率 < 80%

## 文件结构

- `main.py`: 主程序入口 (当前为空)
- `需求.md`: 完整的系统设计文档和实施路线图

## 开发指南

在开发此项目时，需要特别关注：
1. 实时性要求严格，每个组件都有明确的延迟预算
2. 使用量化和模型压缩技术以适应端侧资源限制
3. 建立完善的测试集，包括标准指令、口语化指令、模糊指令和负样本
4. 设计 OTA 更新机制，支持增量更新技能库而无需重训模型
