# Qwen3-1.7B 集成指南

本文档详细说明了如何将 Qwen3-1.7B 模型集成到车控语音助手系统中，替代原来的 Gemma 3n E2B 模型。

## 模型信息

| 项目 | 详情 |
|------|------|
| 模型名称 | Qwen3-1.7B |
| 开发者 | Alibaba DAMO Academy |
| 模型参数 | 1.7B |
| 量化格式 | Q4_K_M (llama.cpp) |
| 上下文长度 | 2048 tokens |
| 推理速度 | <300ms (在 Qualcomm 8295) |
| 内存占用 | ~4-5GB |
| 部署方式 | llama.cpp 或 Ollama |

## 部署方式

### 1. Ollama 方式（推荐用于开发测试）

#### 安装 Ollama
```bash
# Windows
winget install Ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Mac
brew install ollama
```

#### 下载模型
```bash
ollama pull qwen3:1.7b
```

#### 启动服务
```bash
ollama serve
```

#### 配置使用
```python
from src.hybrid.llm_parser import HybridLLMEngine

config = {
    "use_local": True,
    "base_url": "http://localhost:11434",
    "model_name": "qwen3:1.7b"
}

engine = HybridLLMEngine(config)
```

### 2. llama.cpp 方式（推荐用于生产部署）

#### 下载 GGUF 格式模型
```bash
# 从 Hugging Face 下载量化模型
wget https://huggingface.co/Qwen/Qwen3-1.7B-GGUF/resolve/main/qwen3-1.7b-q4_k_m.gguf
```

#### 编译 llama.cpp
```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make LLAMA_CUBLAS=1  # 如果支持 CUDA
make                 # CPU 版本
```

#### 配置使用
```python
from src.hybrid.llm_parser import HybridLLMEngine

config = {
    "use_local": True,
    "model_path": "/path/to/qwen3-1.7b-q4_k_m.gguf",
    "model_name": "qwen3-1.7b"
}

engine = HybridLLMEngine(config)
```

## 性能优化

### 1. 量化选择
- Q4_K_M：平衡性能和内存占用（推荐）
- Q8_0：更高精度，但占用更多内存
- Q5_K_M：折中选择

### 2. 推理优化
```python
# llama.cpp 参数优化
config = {
    "n_gpu_layers": -1,  # 使用所有可用的 GPU 层
    "n_ctx": 2048,        # 上下文窗口
    "n_threads": 4,       # CPU 线程数
    "n_batch": 512,      # 批处理大小
    "use_mmap": True,     # 内存映射
    "n_threads_batch": 1 # 批处理线程数
}
```

### 3. 高级特性

#### Grammar Constrained Decoding
使用 gbnf 文件约束输出格式：
```python
# grammar.gbnf
root ::= object
object ::= "{" pair "}"
pair ::= string ":" value
value ::= string | number | object | array
```

#### Context Caching
缓存频繁使用的提示词，减少重复计算。

## 测试验证

### 运行测试脚本
```bash
# 运行完整测试
python scripts/test_qwen3_1.7b.py

# 选择特定测试
python scripts/test_qwen3_1.7b.py
# 选择 1: Ollama 测试
# 选择 2: llama.cpp 测试
# 选择 3: API 降级测试
```

### 性能基准

| 部署方式 | 延迟 | 内存 | 准确率 |
|---------|------|------|--------|
| Ollama | ~350ms | ~5GB | >95% |
| llama.cpp | ~280ms | ~4GB | >95% |
| API | ~100ms | - | >95% |

## 常见问题

### 1. 内存不足
- 使用更小的量化版本（如 Q5_K_M）
- 减少上下文窗口长度
- 关闭其他 GPU 应用

### 2. 推理速度慢
- 确保 NPU/CPU 加速可用
- 调整批处理参数
- 使用 Vulkan 加速

### 3. 输出格式错误
- 启用 Grammar Constrained
- 添加明确的输出示例
- 使用 JSON Schema 验证

### 4. 中文理解问题
- 确保使用正确的模型版本（Qwen3 支持）
- 在提示词中指定使用中文
- 增加中文测试案例

## 版本升级

从 Gemma 3n E2B 升级到 Qwen3-1.7B：

### 1. 模型下载
```bash
# 原模型
Gemma 3n E2B (~2.1B, Q4_K_M)

# 新模型
Qwen3-1.7B (1.7B, Q4_K_M)
```

### 2. 配置更新
- 更新模型路径
- 调整参数配置
- 更新提示词模板

### 3. 性能对比
- 参数更少，推理更快
- 中文理解能力更强
- 支持更多量化格式

## 监控和维护

### 1. 资源监控
```python
import psutil

def monitor_resources():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    print(f"CPU: {cpu}%, Memory: {memory}%")
```

### 2. 日志记录
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 3. 定期备份
- 定期备份模型文件
- 保存推理日志
- 备份配置文件

## 联系支持

如有问题，请参考：
- Hugging Face 模型页面：https://huggingface.co/Qwen/Qwen3-1.7B
- llama.cpp 文档：https://github.com/ggerganov/llama.cpp
- Ollama 文档：https://ollama.com