"""
引擎配置模块
支持多种 LLM 部署方式的统一配置
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """LLM 配置"""
    provider: str = "rule"  # rule, ollama, llama_cpp, api
    model_name: str = "qwen3-1.7b"
    model_path: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    use_local: bool = False

    # Ollama 特定配置
    ollama_timeout: int = 60

    # llama.cpp 特定配置
    n_gpu_layers: int = -1
    n_ctx: int = 2048
    n_threads: int = 4
    n_batch: int = 512
    use_mmap: bool = True
    use_mlock: bool = False

    # API 特定配置
    api_base: Optional[str] = None
    api_provider: Optional[str] = None  # qwen, deepseek, openai


class EngineConfig:
    """引擎主配置"""

    def __init__(self, config_file: Optional[str] = None):
        """初始化配置"""
        self.config_file = config_file or "config/engine_config.json"
        self.llm_config = self._load_config()

        # 从环境变量读取 API 密钥
        self._load_env_credentials()

    def _load_config(self) -> LLMConfig:
        """加载配置文件"""
        default_config = {
            "provider": "rule",
            "model_name": "qwen3-1.7b",
            "model_path": None,
            "base_url": None,
            "api_key": None,
            "temperature": 0.7,
            "max_tokens": 1000,
            "use_local": False,
            "ollama_timeout": 60,
            "n_gpu_layers": -1,
            "n_ctx": 2048,
            "n_threads": 4,
            "n_batch": 512,
            "use_mmap": True,
            "use_mlock": False,
            "api_base": None,
            "api_provider": "qwen"
        }

        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)

                # 更新默认配置
                for key, value in config_data.items():
                    if hasattr(LLMConfig, key):
                        default_config[key] = value
            except Exception as e:
                print(f"加载配置文件失败，使用默认配置: {e}")

        return LLMConfig(**default_config)

    def _load_env_credentials(self):
        """从环境变量加载凭据"""
        # API 密钥
        if not self.llm_config.api_key:
            self.llm_config.api_key = os.getenv("DASHSCOPE_API_KEY")  # Qwen
            if not self.llm_config.api_key:
                self.llm_config.api_key = os.getenv("DEEPSEEK_API_KEY")  # DeepSeek
            if not self.llm_config.api_key:
                self.llm_config.api_key = os.getenv("OPENAI_API_KEY")  # OpenAI

        # Ollama 地址
        if not self.llm_config.base_url:
            self.llm_config.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def get_llm_parser_kwargs(self) -> Dict[str, Any]:
        """获取 LLM 解析器参数"""
        kwargs = {
            "use_local_llm": self.llm_config.use_local or self.llm_config.provider in ["ollama", "llama_cpp"],
            "model_path": self.llm_config.model_path,
            "api_key": self.llm_config.api_key,
            "base_url": self.llm_config.base_url,
            "model_name": self.llm_config.model_name
        }

        # 只包含非 None 的参数
        return {k: v for k, v in kwargs.items() if v is not None}

    def is_llm_enabled(self) -> bool:
        """检查是否启用了 LLM"""
        return self.llm_config.provider != "rule"

    def is_local_llm(self) -> bool:
        """检查是否使用本地 LLM"""
        return self.llm_config.use_local or self.llm_config.provider in ["ollama", "llama_cpp"]

    def get_provider_info(self) -> str:
        """获取提供商信息"""
        provider = self.llm_config.provider

        if provider == "rule":
            return "规则引擎（无 LLM）"
        elif provider == "ollama":
            return f"Ollama ({self.llm_config.model_name})"
        elif provider == "llama_cpp":
            return f"llama.cpp ({self.llm_config.model_name})"
        elif provider == "api":
            return f"API ({self.llm_config.api_provider})"
        else:
            return "未知提供商"

    def save_config(self):
        """保存配置到文件"""
        config_data = {
            "provider": self.llm_config.provider,
            "model_name": self.llm_config.model_name,
            "model_path": self.llm_config.model_path,
            "base_url": self.llm_config.base_url,
            "api_key": self.llm_config.api_key,
            "temperature": self.llm_config.temperature,
            "max_tokens": self.llm_config.max_tokens,
            "use_local": self.llm_config.use_local,
            "ollama_timeout": self.llm_config.ollama_timeout,
            "n_gpu_layers": self.llm_config.n_gpu_layers,
            "n_ctx": self.llm_config.n_ctx,
            "n_threads": self.llm_config.n_threads,
            "n_batch": self.llm_config.n_batch,
            "use_mmap": self.llm_config.use_mmap,
            "use_mlock": self.llm_config.use_mlock,
            "api_base": self.llm_config.api_base,
            "api_provider": self.llm_config.api_provider
        }

        # 确保配置目录存在
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        print(f"配置已保存到: {config_path}")


def create_default_config():
    """创建默认配置文件"""
    config = EngineConfig()
    config.save_config()
    return config


# 预定义的配置模板
CONFIG_TEMPLATES = {
    "rule_only": {
        "provider": "rule",
        "model_name": "qwen3-1.7b",
        "use_local": False
    },
    "ollama_development": {
        "provider": "ollama",
        "model_name": "qwen3:1.7b",
        "base_url": "http://localhost:11434",
        "use_local": True,
        "ollama_timeout": 60
    },
    "llama_cpp_production": {
        "provider": "llama_cpp",
        "model_name": "qwen3-1.7b",
        "model_path": "models/qwen3-1.7b-q4_k_m.gguf",
        "use_local": True,
        "n_gpu_layers": -1,
        "n_ctx": 2048
    },
    "api_cloud": {
        "provider": "api",
        "api_provider": "qwen",
        "model_name": "qwen-turbo",
        "use_local": False
    }
}


def apply_template(template_name: str, config_file: str = "config/engine_config.json"):
    """应用预定义配置模板"""
    if template_name not in CONFIG_TEMPLATES:
        raise ValueError(f"未知的模板: {template_name}")

    template = CONFIG_TEMPLATES[template_name]
    config = EngineConfig()

    # 更新配置
    for key, value in template.items():
        setattr(config.llm_config, key, value)

    config.config_file = config_file
    config.save_config()

    print(f"已应用配置模板: {template_name}")
    print(f"LLM 提供商: {config.get_provider_info()}")

    return config


if __name__ == "__main__":
    # 创建默认配置
    config = create_default_config()
    print(f"默认配置: {config.get_provider_info()}")

    # 应用不同模板
    print("\n可用配置模板:")
    for name in CONFIG_TEMPLATES:
        print(f"  - {name}: {CONFIG_TEMPLATES[name]['provider']}")