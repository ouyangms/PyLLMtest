# LLM API 配置指南

本项目支持多种 LLM API 来生成高质量训练样本。

## 支持的 LLM 服务

### 1. OpenAI API

**模型**: gpt-3.5-turbo, gpt-4o, gpt-4o-mini

**配置方法**:
```bash
# Windows
set OPENAI_API_KEY=sk-your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=sk-your-api-key-here
```

**获取 API Key**: https://platform.openai.com/api-keys

**使用示例**:
```bash
python scripts/generate_queries_llm.py --provider openai --model gpt-3.5-turbo
```

**费用参考** (gpt-3.5-turbo):
- 输入: $0.50 / 1M tokens
- 输出: $1.50 / 1M tokens
- 预估成本: ~$2-5 (生成 5000 个技能样本)

---

### 2. 通义千问 (DashScope)

**模型**: qwen-turbo, qwen-plus, qwen-max

**配置方法**:
```bash
# Windows
set DASHSCOPE_API_KEY=sk-your-api-key-here

# Linux/Mac
export DASHSCOPE_API_KEY=sk-your-api-key-here
```

**获取 API Key**: https://dashscope.console.aliyun.com/apiKey

**使用示例**:
```bash
python scripts/generate_queries_llm.py --provider qwen --model qwen-turbo
```

**费用参考** (qwen-turbo):
- 输入: ¥0.0008 / 千 tokens
- 输出: ¥0.002 / 千 tokens
- 预估成本: ~¥10-30 (生成 5000 个技能样本)

**优势**:
- 国内服务，延迟低
- 中文能力强
- 新用户通常有免费额度

---

### 3. DeepSeek

**模型**: deepseek-chat, deepseek-coder

**配置方法**:
```bash
# Windows
set DEEPSEEK_API_KEY=sk-your-api-key-here

# Linux/Mac
export DEEPSEEK_API_KEY=sk-your-api-key-here
```

**获取 API Key**: https://platform.deepseek.com/api_keys

**使用示例**:
```bash
python scripts/generate_queries_llm.py --provider deepseek --model deepseek-chat
```

**费用参考**:
- 输入: ¥1 / 1M tokens
- 输出: ¥2 / 1M tokens
- 预估成本: ~¥5-15 (生成 5000 个技能样本)

**优势**:
- 极具竞争力的价格
- 中文能力强
- API 兼容 OpenAI 格式

---

### 4. Ollama (本地模型)

**模型**: qwen2:7b, llama3:8b, gemma2:9b 等

**配置方法**:
1. 安装 Ollama: https://ollama.ai
2. 拉取模型: `ollama pull qwen2:7b`
3. 启动服务: `ollama serve`

**使用示例**:
```bash
python scripts/generate_queries_llm.py --provider ollama --model qwen2:7b
```

**优势**:
- 完全免费
- 数据隐私
- 可离线使用

**劣势**:
- 需要较好的硬件（推荐 GPU）
- 生成速度较慢
- 质量可能不如云端模型

---

## 推荐方案

### 快速测试
```bash
# 使用通义千问（国内推荐）
python scripts/generate_queries_llm.py --provider qwen --test --target-count 5
```

### 完整生成
```bash
# 使用 DeepSeek（性价比高）
python scripts/generate_queries_llm.py --provider deepseek --target-count 8

# 或使用 Ollama（免费但慢）
python scripts/generate_queries_llm.py --provider ollama --model qwen2:7b --target-count 8
```

### 断点续传
```bash
# 如果生成中断，可以从上次位置继续
python scripts/generate_queries_llm.py \
    --provider qwen \
    --start-index 100 \
    --resume-file data/processed/skills_llm_enhanced.tmp.json
```

---

## 环境变量持久化

### Windows PowerShell
创建 `$env:OPENAI_API_KEY` 在系统环境变量中，或添加到配置文件：
```powershell
# 临时设置
$env:OPENAI_API_KEY="sk-your-key"

# 永久设置
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-your-key', 'User')
```

### Windows CMD
```cmd
setx OPENAI_API_KEY "sk-your-key"
```

### Linux/Mac
添加到 `~/.bashrc` 或 `~/.zshrc`:
```bash
export OPENAI_API_KEY="sk-your-key"
export DASHSCOPE_API_KEY="sk-your-key"
```

---

## 故障排除

### 连接超时
- 检查网络连接
- 使用国内服务（通义千问）
- 尝试使用 VPN

### API Key 无效
- 确认 API key 是否正确复制
- 检查 API key 是否过期
- 确认账户有足够余额

### 生成质量差
- 调整 temperature 参数（0.7-0.9）
- 使用更强的模型（如 qwen-plus, gpt-4o）
- 优化 Prompt 模板

### 速度太慢
- 减小 batch_size
- 使用更快的模型（如 qwen-turbo）
- 使用本地 Ollama（需 GPU）
