#!/usr/bin/env python3
"""
配置管理脚本
管理 Qwen3-1.7B 的各种部署配置
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.engine_config import EngineConfig, apply_template, CONFIG_TEMPLATES


def show_config():
    """显示当前配置"""
    config = EngineConfig()

    print("=" * 60)
    print("当前配置")
    print("=" * 60)

    print(f"\n[基本信息]")
    print(f"  提供商: {config.llm_config.provider}")
    print(f"  模型名称: {config.llm_config.model_name}")
    print(f"  使用本地LLM: {config.llm_config.use_local}")

    print(f"\n[部署信息]")
    if config.llm_config.provider == "ollama":
        print(f"  Ollama 地址: {config.llm_config.base_url}")
        print(f"  超时时间: {config.llm_config.ollama_timeout}s")
    elif config.llm_config.provider == "llama_cpp":
        print(f"  模型路径: {config.llm_config.model_path}")
        print(f"  GPU层数: {config.llm_config.n_gpu_layers}")
        print(f"  上下文长度: {config.llm_config.n_ctx}")
    elif config.llm_config.provider == "api":
        print(f"  API提供商: {config.llm_config.api_provider}")
        print(f"  API基础URL: {config.llm_config.api_base}")
        if config.llm_config.api_key:
            print(f"  API密钥: 已配置")
        else:
            print(f"  API密钥: 未配置")

    print(f"\n[性能参数]")
    print(f"  温度: {config.llm_config.temperature}")
    print(f"  最大tokens: {config.llm_config.max_tokens}")
    print(f"  线程数: {config.llm_config.n_threads}")

    print(f"\n[状态]")
    print(f"  LLM已启用: {config.is_llm_enabled()}")
    print(f"  使用本地部署: {config.is_local_llm()}")


def list_templates():
    """列出所有可用配置模板"""
    print("=" * 60)
    print("可用配置模板")
    print("=" * 60)

    for name, template in CONFIG_TEMPLATES.items():
        print(f"\n{name}:")
        print(f"  提供商: {template['provider']}")
        print(f"  模型: {template.get('model_name', 'N/A')}")
        if 'base_url' in template:
            print(f"  地址: {template['base_url']}")
        if 'api_provider' in template:
            print(f"  API: {template['api_provider']}")


def setup_config(template_name=None, custom_config=None):
    """设置配置"""
    if template_name:
        if template_name not in CONFIG_TEMPLATES:
            print(f"错误: 未知的模板 '{template_name}'")
            list_templates()
            return False

        apply_template(template_name)
        print(f"✓ 已应用配置模板: {template_name}")
    elif custom_config:
        # 应用自定义配置
        config = EngineConfig()
        for key, value in custom_config.items():
            if hasattr(config.llm_config, key):
                setattr(config.llm_config, key, value)

        config.save_config()
        print("✓ 已应用自定义配置")
    else:
        # 使用默认配置
        config = EngineConfig()
        config.save_config()
        print("✓ 已使用默认配置")

    show_config()
    return True


def test_config():
    """测试配置是否可用"""
    print("=" * 60)
    print("测试配置")
    print("=" * 60)

    config = EngineConfig()

    if not config.is_llm_enabled():
        print("当前配置使用规则引擎，无需测试连接")
        return True

    print(f"测试 {config.get_provider_info()}...")

    try:
        if config.llm_config.provider == "ollama":
            import requests
            response = requests.get(
                f"{config.llm_config.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json().get("models", [])
                if any(config.llm_config.model_name.replace(":", "-") in m["name"] for m in models):
                    print("✓ Ollama 连接成功，模型已安装")
                else:
                    print("✓ Ollama 连接成功，但模型未安装")
                    print(f"  需要运行: ollama pull {config.llm_config.model_name}")
                    return False
            else:
                print(f"✗ Ollama 连接失败: {response.status_code}")
                return False

        elif config.llm_config.provider == "api":
            if not config.llm_config.api_key:
                print("✗ API密钥未配置")
                print("请设置环境变量:")
                if config.llm_config.api_provider == "qwen":
                    print("  export DASHSCOPE_API_KEY='your_key'")
                elif config.llm_config.api_provider == "deepseek":
                    print("  export DEEPSEEK_API_KEY='your_key'")
                elif config.llm_config.api_provider == "openai":
                    print("  export OPENAI_API_KEY='your_key'")
                return False
            else:
                print("✓ API密钥已配置")

        elif config.llm_config.provider == "llama_cpp":
            if not config.llm_config.model_path or not Path(config.llm_config.model_path).exists():
                print("✗ 模型文件不存在")
                print(f"  请将模型文件放在: {config.llm_config.model_path}")
                return False
            else:
                print("✓ 模型文件存在")

        print("✓ 配置测试通过")
        return True

    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def quick_setup():
    """快速设置向导"""
    print("=" * 60)
    print("快速设置向导")
    print("=" * 60)

    print("\n请选择部署方式:")
    print("1. 规则引擎（最快，无需额外安装）")
    print("2. Ollama（本地部署，需要安装Ollama）")
    print("3. API云端部署（需要API密钥）")
    print("4. llama.cpp（高性能本地部署）")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == "1":
        setup_config("rule_only")
    elif choice == "2":
        print("\n请确保已安装 Ollama 并下载了模型:")
        print("  1. 安装 Ollama: https://ollama.com/")
        print("  2. 下载模型: ollama pull qwen3:1.7b")
        setup_config("ollama_development")
    elif choice == "3":
        provider = input("选择 API 提供商 (qwen/deepseek/openai): ").strip()
        if provider in ["qwen", "deepseek", "openai"]:
            config = EngineConfig()
            config.llm_config.provider = "api"
            config.llm_config.api_provider = provider
            config.llm_config.model_name = f"{provider}-turbo" if provider == "qwen" else f"{provider}-chat"
            config.save_config()
            print(f"✓ 已设置为 {provider} API")
        else:
            print("无效的提供商选择")
    elif choice == "4":
        model_path = input("输入 GGUF 模型路径: ").strip()
        if model_path:
            setup_config("llama_cpp_production", {"model_path": model_path})
        else:
            print("模型路径不能为空")
    else:
        print("无效选择")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="配置管理脚本")
    parser.add_argument("command", choices=["show", "list", "setup", "test", "quick"],
                       help="命令")
    parser.add_argument("--template", help="配置模板名称")
    parser.add_argument("--key-value", nargs="*", help="自定义配置 (key=value)")

    args = parser.parse_args()

    if args.command == "show":
        show_config()
    elif args.command == "list":
        list_templates()
    elif args.command == "setup":
        custom_config = {}
        if args.key_value:
            for item in args.key_value:
                if "=" in item:
                    key, value = item.split("=", 1)
                    custom_config[key] = value
        setup_config(args.template, custom_config)
    elif args.command == "test":
        test_config()
    elif args.command == "quick":
        quick_setup()


if __name__ == "__main__":
    main()