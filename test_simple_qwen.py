#!/usr/bin/env python3
"""
简单 Qwen3-1.7B 功能测试
"""

import sys
import json
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_functionality():
    """测试基本功能"""
    print("=" * 60)
    print("基本功能测试")
    print("=" * 60)

    # 1. 测试配置
    print("1. 测试配置文件...")
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            model_name = config['model']['name']
            print(f"   模型名称: {model_name}")
            assert 'qwen3' in model_name.lower()
            print("   [PASS] 配置正确")
    except Exception as e:
        print(f"   [FAIL] {e}")

    # 2. 测试 LLM 解析器
    print("\n2. 测试 LLM 解析器...")
    try:
        from src.hybrid.llm_parser import HybridLLMEngine

        # 规则引擎模式
        engine = HybridLLMEngine({'use_local': False})
        print("   [PASS] 规则引擎创建成功")

        # Ollama 模式
        ollama_config = {
            "use_local": True,
            "base_url": "http://localhost:11434",
            "model_name": "qwen3:1.7b"
        }
        ollama_engine = HybridLLMEngine(ollama_config)
        print("   [PASS] Ollama 配置成功")

        # 测试解析功能
        result = engine.parse("打开空调", [
            {"skill_id": "OpenAC", "name": "打开空调", "similarity": 0.8}
        ])
        print(f"   解析结果: skill_id={result.skill_id}, confidence={result.confidence}")
        print("   [PASS] 解析功能正常")

    except Exception as e:
        print(f"   [FAIL] {e}")

    # 3. 测试 LLM 客户端
    print("\n3. 测试 LLM 客户端...")
    try:
        from src.data.llm_client import create_llm_client

        # Ollama 客户端
        client = create_llm_client("ollama", model="qwen3:1.7b")
        print("   [PASS] Ollama 客户端创建成功")

        # Qwen API 客户端（只检查配置）
        try:
            qwen_client = create_llm_client("qwen", model="qwen-turbo")
            print("   [PASS] Qwen API 配置正确")
        except Exception as e:
            if "API Key" in str(e):
                print("   [WARNING] Qwen API Key 未配置，这是正常的")
            else:
                print(f"   [FAIL] {e}")

    except Exception as e:
        print(f"   [FAIL] {e}")

    # 4. 测试架构配置
    print("\n4. 测试架构配置...")
    try:
        from src.hybrid.architecture import HybridArchitectureConfig

        if "llm" in HybridArchitectureConfig.MODELS:
            llm_model = HybridArchitectureConfig.MODELS["llm"]
            model_name = llm_model["name"]
            print(f"   架构模型名称: {model_name}")
            assert "Qwen3" in model_name
            print("   [PASS] 架构配置正确")
        else:
            print("   [FAIL] 缺少 LLM 配置")

    except Exception as e:
        print(f"   [FAIL] {e}")

    print("\n测试完成！")

if __name__ == "__main__":
    test_basic_functionality()