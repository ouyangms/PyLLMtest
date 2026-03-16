#!/usr/bin/env python3
"""
Qwen3-1.7B 集成测试脚本
"""

import sys
import json
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_config_update():
    """测试配置文件更新"""
    print("=" * 50)
    print("1. 测试配置文件更新")
    print("=" * 50)

    # 检查配置文件
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        model_name = config["model"]["name"]
        if "qwen3" in model_name.lower():
            print("[PASS] 配置文件中已更新为 Qwen3-1.7B")
            print(f"  模型名称: {model_name}")
            return True
        else:
            print("[FAIL] 配置文件中未找到 Qwen3-1.7B")
            return False
    else:
        print("[FAIL] 配置文件不存在")
        return False

def test_llm_parser():
    """测试 LLM 解析器"""
    print("\n" + "=" * 50)
    print("2. 测试 LLM 解析器")
    print("=" * 50)

    try:
        from src.hybrid.llm_parser import HybridLLMEngine

        # 测试规则引擎
        config = {"use_local": False}
        engine = HybridLLMEngine(config)
        print("[PASS] HybridLLMEngine 创建成功")

        # 测试 Ollama 配置
        ollama_config = {
            "use_local": True,
            "base_url": "http://localhost:11434",
            "model_name": "qwen3:1.7b"
        }
        ollama_engine = HybridLLMEngine(ollama_config)
        print("[PASS] Ollama 引擎配置成功")

        # 测试 llama.cpp 配置
        llama_config = {
            "use_local": True,
            "model_path": "test_model.gguf",
            "model_name": "qwen3-1.7b"
        }
        llama_engine = HybridLLMEngine(llama_config)
        print("[PASS] llama.cpp 引擎配置成功")

        return True
    except Exception as e:
        print(f"✗ LLM 解析器测试失败: {e}")
        return False

def test_llm_client():
    """测试 LLM 客户端"""
    print("\n" + "=" * 50)
    print("3. 测试 LLM 客户端")
    print("=" * 50)

    try:
        from src.data.llm_client import create_llm_client

        # 测试 Ollama 客户端
        ollama_client = create_llm_client("ollama", model="qwen3:1.7b")
        print("[PASS] Ollama 客户端创建成功")

        # 测试 Qwen API 客户端配置
        qwen_client_config = create_llm_client("qwen", model="qwen-turbo")
        print("[PASS] Qwen API 客户端配置成功")

        return True
    except Exception as e:
        print(f"✗ LLM 客户端测试失败: {e}")
        return False

def test_architecture():
    """测试架构文档"""
    print("\n" + "=" * 50)
    print("4. 测试架构文档")
    print("=" * 50)

    try:
        from src.hybrid.architecture import HybridArchitectureConfig

        # 检查模型配置
        if "llm" in HybridArchitectureConfig.MODELS:
            llm_config = HybridArchitectureConfig.MODELS["llm"]
            if "Qwen3-1.7B" in llm_config["name"]:
                print("[PASS] 架构配置中已更新为 Qwen3-1.7B")
                print(f"  模型名称: {llm_config['name']}")
                print(f"  部署方式: {llm_config['deployment']}")
                return True
            else:
                print("[FAIL] 架构配置中未找到 Qwen3-1.7B")
                return False
        else:
            print("[FAIL] 架构配置中缺少 LLM 配置")
            return False
    except Exception as e:
        print(f"✗ 架构文档测试失败: {e}")
        return False

def test_requirements():
    """测试需求文档"""
    print("\n" + "=" * 50)
    print("5. 测试需求文档")
    print("=" * 50)

    requirements_path = Path("需求.md")
    if requirements_path.exists():
        with open(requirements_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "Qwen3-1.7B" in content:
            print("[PASS] 需求文档中已更新为 Qwen3-1.7B")
            return True
        else:
            print("[FAIL] 需求文档中未找到 Qwen3-1.7B")
            return False
    else:
        print("[FAIL] 需求文档不存在")
        return False

def main():
    """主测试函数"""
    print("Qwen3-1.7B 集成测试")
    print("=" * 70)

    tests = [
        ("配置文件更新", test_config_update),
        ("LLM 解析器", test_llm_parser),
        ("LLM 客户端", test_llm_client),
        ("架构文档", test_architecture),
        ("需求文档", test_requirements)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n{test_name} 测试异常: {e}")
            results.append((test_name, False))

    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)

    passed = 0
    for test_name, result in results:
        status = "[PASS] 通过" if result else "[FAIL] 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n总计: {passed}/{len(results)} 项测试通过")

    if passed == len(results):
        print("\n🎉 所有测试通过！Qwen3-1.7B 集成成功！")
    else:
        print("\n⚠️  部分测试失败，请检查相关配置")

if __name__ == "__main__":
    main()