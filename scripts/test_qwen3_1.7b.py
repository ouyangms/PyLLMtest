#!/usr/bin/env python3
"""
Qwen3-1.7B 本地模型测试脚本
支持 llama.cpp 和 Ollama 两种部署方式
"""

import json
import sys
import time
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.hybrid.llm_parser import HybridLLMEngine
from src.data.llm_client import create_llm_client


def test_ollama_qwen3():
    """测试通过 Ollama 部署的 Qwen3-1.7B"""
    print("=" * 70)
    print("测试 Ollama + Qwen3-1.7B")
    print("=" * 70)

    # 配置
    config = {
        "use_local": True,
        "base_url": "http://localhost:11434",
        "model_name": "qwen3:1.7b"
    }

    try:
        # 创建引擎
        engine = HybridLLMEngine(config)

        # 测试用例
        test_cases = [
            {
                "user_input": "打开空调，温度调到24度",
                "candidates": [
                    {
                        "skill_id": "OpenAC",
                        "name": "打开空调",
                        "description": "打开空调系统",
                        "params_schema": {"action": "string"}
                    },
                    {
                        "skill_id": "SetTemperature",
                        "name": "设置温度",
                        "description": "设置空调到指定温度",
                        "params_schema": {"temperature": "integer"}
                    }
                ]
            },
            {
                "user_input": "打开主驾驶车窗",
                "candidates": [
                    {
                        "skill_id": "OpenWindow",
                        "name": "打开车窗",
                        "description": "打开指定位置的车窗",
                        "params_schema": {"position": "string"}
                    }
                ]
            }
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n测试用例 {i}:")
            print(f"用户输入: {test_case['user_input']}")
            print(f"候选技能数: {len(test_case['candidates'])}")

            start_time = time.time()
            result = engine.parse(
                test_case['user_input'],
                test_case['candidates']
            )
            end_time = time.time()

            print(f"\n解析结果:")
            print(f"  - 技能ID: {result.skill_id}")
            print(f"  - 置信度: {result.confidence:.2f}")
            print(f"  - 参数: {result.parameters}")
            print(f"  - 推理: {result.reasoning}")
            print(f"  - 耗时: {(end_time - start_time) * 1000:.2f}ms")

    except Exception as e:
        print(f"测试失败: {e}")


def test_llamacpp_qwen3():
    """测试通过 llama.cpp 部署的 Qwen3-1.7B"""
    print("\n" + "=" * 70)
    print("测试 llama.cpp + Qwen3-1.7B")
    print("=" * 70)

    # 配置
    config = {
        "use_local": True,
        "model_path": "path/to/qwen3-1.7b-q4_k_m.gguf",  # 需要下载模型文件
        "base_url": None,
        "model_name": "qwen3-1.7b"
    }

    try:
        # 创建引擎
        engine = HybridLLMEngine(config)

        # 测试用例
        test_case = {
            "user_input": "把空调温度调低一点",
            "candidates": [
                {
                    "skill_id": "SetTemperature",
                    "name": "设置温度",
                    "description": "调节空调温度",
                    "params_schema": {"temperature": "integer"}
                }
            ]
        }

        print(f"用户输入: {test_case['user_input']}")
        print("注意：此测试需要先下载 Qwen3-1.7B GGUF 格式模型")

        start_time = time.time()
        result = engine.parse(
            test_case['user_input'],
            test_case['candidates']
        )
        end_time = time.time()

        print(f"\n解析结果:")
        print(f"  - 技能ID: {result.skill_id}")
        print(f"  - 置信度: {result.confidence:.2f}")
        print(f"  - 参数: {result.parameters}")
        print(f"  - 推理: {result.reasoning}")
        print(f"  - 耗时: {(end_time - start_time) * 1000:.2f}ms")

    except Exception as e:
        print(f"测试失败: {e}")


def test_api_fallback():
    """测试 API 降级方案"""
    print("\n" + "=" * 70)
    print("测试 API 降级方案")
    print("=" * 70)

    # 测试不同的 API 提供商
    providers = [
        ("qwen", "qwen-turbo"),
        ("deepseek", "deepseek-chat"),
        ("openai", "gpt-3.5-turbo")
    ]

    for provider, default_model in providers:
        print(f"\n测试 {provider} API:")

        try:
            client = create_llm_client(
                provider=provider,
                model=default_model
            )

            test_prompt = """请解析用户意图并返回JSON格式结果：
用户输入: "打开空调，调到24度"
候选技能:
1. skill_id: "OpenAC", name: "打开空调", params: {"action": "string"}
2. skill_id: "SetTemperature", name: "设置温度", params: {"temperature": "integer"}

请返回:
{
    "skill_id": "技能ID",
    "parameters": {"参数": "值"},
    "confidence": 0.95,
    "reasoning": "选择原因"
}"""

            print("  调用中...")
            response = client.generate(test_prompt, max_tokens=500)
            print(f"  成功: {response[:100]}...")

        except Exception as e:
            print(f"  失败: {e}")


def main():
    """主函数"""
    print("Qwen3-1.7B 车控语音助手测试")
    print("支持测试:")
    print("1. Ollama 本地部署")
    print("2. llama.cpp 本地部署")
    print("3. API 降级方案")

    choice = input("\n请选择测试模式 (1/2/3/all): ").strip()

    if choice in ["1", "all"]:
        test_ollama_qwen3()
    if choice in ["2", "all"]:
        test_llamacpp_qwen3()
    if choice in ["3", "all"]:
        test_api_fallback()


if __name__ == "__main__":
    main()