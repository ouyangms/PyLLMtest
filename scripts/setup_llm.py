"""
LLM API 配置向导
帮助用户设置和测试 LLM API 连接
"""

import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.llm_client import create_llm_client


def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_section(text):
    print("\n" + "-" * 60)
    print(text)
    print("-" * 60)


def test_provider(provider, api_key, model=None):
    """测试 LLM 提供商连接"""
    print(f"\n测试 {provider}...")

    try:
        client = create_llm_client(
            provider=provider,
            api_key=api_key,
            model=model
        )

        # 测试生成
        test_prompt = "请为'打开空调'生成 3 种不同的口语化表达，每条不超过 8 个字。只返回列表，格式如：['表达1', '表达2', '表达3']"

        print("发送测试请求...")
        response = client.generate(test_prompt, max_tokens=200)

        print(f"\n响应:\n{response}")
        return True

    except Exception as e:
        print(f"\n[失败] {e}")
        return False


def interactive_setup():
    """交互式配置"""
    print_header("LLM API 配置向导")

    print("\n请选择 LLM 服务提供商:")
    print("  1. 通义千问 (DashScope) - 推荐，国内服务")
    print("  2. DeepSeek - 高性价比")
    print("  3. OpenAI - 需要网络环境")
    print("  4. Ollama - 本地模型")
    print("  5. 跳过")

    choice = input("\n请输入选项 (1-5): ").strip()

    if choice == "1":
        provider = "qwen"
        env_key = "DASHSCOPE_API_KEY"
        default_model = "qwen-turbo"

        print_section("通义千问配置")
        print("\n1. 访问 https://dashscope.console.aliyun.com/apiKey")
        print("2. 创建或复制您的 API Key")
        print("3. 粘贴到下方")

        api_key = input("\n请输入 API Key: ").strip()

        if api_key:
            # 临时设置环境变量
            os.environ[env_key] = api_key

            if test_provider(provider, api_key):
                print(f"\n[成功] {provider} 连接正常!")

                save = input("\n是否保存到环境变量? (y/n): ").strip().lower()
                if save == "y":
                    print(f"\n请将以下内容添加到系统环境变量:")
                    print(f"  {env_key}={api_key}")

                    if os.name == 'nt':  # Windows
                        print("\n或使用命令:")
                        print(f"  setx {env_key} {api_key}")
                    else:  # Linux/Mac
                        print("\n或添加到 ~/.bashrc:")
                        print(f"  export {env_key}={api_key}")

                return provider, api_key, default_model

    elif choice == "2":
        provider = "deepseek"
        env_key = "DEEPSEEK_API_KEY"
        default_model = "deepseek-chat"

        print_section("DeepSeek 配置")
        print("\n1. 访问 https://platform.deepseek.com/api_keys")
        print("2. 创建或复制您的 API Key")
        print("3. 粘贴到下方")

        api_key = input("\n请输入 API Key: ").strip()

        if api_key:
            os.environ[env_key] = api_key

            if test_provider(provider, api_key):
                print(f"\n[成功] {provider} 连接正常!")

                save = input("\n是否保存到环境变量? (y/n): ").strip().lower()
                if save == "y":
                    print(f"\n请将以下内容添加到系统环境变量:")
                    print(f"  {env_key}={api_key}")

                return provider, api_key, default_model

    elif choice == "3":
        provider = "openai"
        env_key = "OPENAI_API_KEY"
        default_model = "gpt-3.5-turbo"

        print_section("OpenAI 配置")
        print("\n1. 访问 https://platform.openai.com/api-keys")
        print("2. 创建或复制您的 API Key")
        print("3. 粘贴到下方")

        api_key = input("\n请输入 API Key: ").strip()

        if api_key:
            os.environ[env_key] = api_key

            if test_provider(provider, api_key):
                print(f"\n[成功] {provider} 连接正常!")

                save = input("\n是否保存到环境变量? (y/n): ").strip().lower()
                if save == "y":
                    print(f"\n请将以下内容添加到系统环境变量:")
                    print(f"  {env_key}={api_key}")

                return provider, api_key, default_model

    elif choice == "4":
        provider = "ollama"
        default_model = "qwen2:7b"

        print_section("Ollama 配置")
        print("\n请确保:")
        print("1. 已安装 Ollama: https://ollama.ai")
        print("2. 已下载模型: ollama pull qwen2:7b")
        print("3. 服务正在运行: ollama serve")

        model = input(f"\n模型名称 (默认: {default_model}): ").strip()
        if not model:
            model = default_model

        if test_provider(provider, None, model):
            print(f"\n[成功] {provider} 连接正常!")
            return provider, None, model

    return None, None, None


def quick_test():
    """快速测试现有配置"""
    print_header("快速测试 LLM API")

    providers = [
        ("qwen", os.getenv("DASHSCOPE_API_KEY")),
        ("deepseek", os.getenv("DEEPSEEK_API_KEY")),
        ("openai", os.getenv("OPENAI_API_KEY")),
    ]

    available = []
    for provider, key in providers:
        if key:
            available.append((provider, key))
            print(f"  [{provider.upper()}] API Key 已配置")
        else:
            print(f"  [{provider.upper()}] 未配置")

    if not available:
        print("\n未找到任何 API Key 配置")
        print("请使用交互式配置: python scripts/setup_llm.py --interactive")
        return

    print("\n测试已配置的服务...")
    for provider, key in available:
        test_provider(provider, key)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="LLM API 配置向导")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="交互式配置"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="快速测试"
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "qwen", "deepseek", "ollama"],
        help="直接测试指定提供商"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_setup()
    elif args.provider:
        api_key = os.getenv(f"{args.provider.upper()}_API_KEY") or os.getenv("DASHSCOPE_API_KEY" if args.provider == "qwen" else "")
        test_provider(args.provider, api_key)
    elif args.test:
        quick_test()
    else:
        # 默认行为
        if os.getenv("OPENAI_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("DEEPSEEK_API_KEY"):
            quick_test()
        else:
            print("未检测到 API Key 配置")
            print("\n使用 --interactive 开始配置，或查看 LLM_API_SETUP.md 了解详情")


if __name__ == "__main__":
    main()
