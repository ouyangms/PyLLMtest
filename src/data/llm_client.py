"""
LLM 客户端接口
支持多种 LLM API 用于生成训练样本
"""

import json
import os
from typing import List, Dict, Optional, Union
from pathlib import Path


class LLMClient:
    """LLM API 客户端基类"""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = None
    ):
        """
        初始化 LLM 客户端

        Args:
            api_key: API 密钥
            base_url: API 基础 URL
            model: 模型名称
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        生成文本

        Args:
            prompt: 提示词
            max_tokens: 最大 token 数
            temperature: 温度参数

        Returns:
            生成的文本
        """
        raise NotImplementedError


class OpenAIClient(LLMClient):
    """OpenAI API 客户端"""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-3.5-turbo"
    ):
        super().__init__(api_key, base_url, model)

        # 从环境变量获取
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("需要设置 OPENAI_API_KEY 环境变量")

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """使用 OpenAI API 生成文本"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            raise ImportError("需要安装 openai: pip install openai>=1.0.0")

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的车载语音指令助手，擅长生成各种自然语言表达。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content


class QwenClient(LLMClient):
    """通义千问 API 客户端"""

    def __init__(
        self,
        api_key: str = None,
        model: str = "qwen-turbo"
    ):
        super().__init__(api_key, "https://dashscope.aliyuncs.com/api/v1", model)

        if not self.api_key:
            self.api_key = os.getenv("DASHSCOPE_API_KEY")

        if not self.api_key:
            raise ValueError("需要设置 DASHSCOPE_API_KEY 环境变量")

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """使用通义千问 API 生成文本"""
        try:
            import requests
        except ImportError:
            raise ImportError("需要安装 requests: pip install requests")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 使用 OpenAI 兼容格式
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个专业的车载语音指令助手，擅长生成各种自然语言表达。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        response = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        return result["choices"][0]["message"]["content"]


class DeepSeekClient(LLMClient):
    """DeepSeek API 客户端"""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = "https://api.deepseek.com/v1",
        model: str = "deepseek-chat"
    ):
        super().__init__(api_key, base_url, model)

        if not self.api_key:
            self.api_key = os.getenv("DEEPSEEK_API_KEY")

        if not self.api_key:
            raise ValueError("需要设置 DEEPSEEK_API_KEY 环境变量")

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """使用 DeepSeek API 生成文本"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            raise ImportError("需要安装 openai: pip install openai>=1.0.0")

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的车载语音指令助手，擅长生成各种自然语言表达。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content


class OllamaClient(LLMClient):
    """Ollama 本地模型客户端"""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "qwen2:7b"
    ):
        super().__init__(None, base_url, model)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """使用 Ollama 本地模型生成文本"""
        try:
            import requests
        except ImportError:
            raise ImportError("需要安装 requests: pip install requests")

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=data,
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        return result.get("response", "")


def create_llm_client(
    provider: str = "openai",
    api_key: str = None,
    base_url: str = None,
    model: str = None
) -> LLMClient:
    """
    创建 LLM 客户端

    Args:
        provider: 提供商 (openai, qwen, deepseek, ollama)
        api_key: API 密钥
        base_url: API 基础 URL
        model: 模型名称

    Returns:
        LLM 客户端实例
    """
    provider = provider.lower()

    if provider == "openai":
        return OpenAIClient(api_key=api_key, base_url=base_url, model=model)
    elif provider == "qwen" or provider == "dashscope":
        return QwenClient(api_key=api_key, model=model)
    elif provider == "deepseek":
        return DeepSeekClient(api_key=api_key, base_url=base_url, model=model)
    elif provider == "ollama":
        return OllamaClient(base_url=base_url, model=model)
    else:
        raise ValueError(f"不支持的 LLM 提供商: {provider}")


def main():
    """测试 LLM 客户端"""
    import argparse

    parser = argparse.ArgumentParser(description="LLM 客户端测试")
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        choices=["openai", "qwen", "deepseek", "ollama"],
        help="LLM 提供商"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="模型名称"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="测试模式"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LLM 客户端测试")
    print("=" * 60)

    try:
        client = create_llm_client(provider=args.provider, model=args.model)
        print(f"\n已连接到: {args.provider}")

        if args.test:
            test_prompt = "请为'打开空调'这个指令生成 5 种不同的表达方式，要求包含标准指令、口语化、场景描述等不同类型。"

            print(f"\n测试提示: {test_prompt}")
            print("\n生成中...")

            response = client.generate(test_prompt, max_tokens=500)
            print(f"\n响应:\n{response}")

    except Exception as e:
        print(f"\n错误: {e}")
        print("\n请确保:")
        print("1. 已设置相应的 API key 环境变量")
        print("2. 已安装必要的依赖包")
        print("3. 网络连接正常")


if __name__ == "__main__":
    main()
