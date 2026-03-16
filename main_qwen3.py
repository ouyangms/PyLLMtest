"""
车控技能推理引擎 - 主入口 V3（支持 Qwen3-1.7B）
完整6阶段流程：用户输入 → 路由分类 → 技能检索 → LLM解析 → 技能执行 → 输出结果

使用示例:
    python main_qwen3.py "打开空调"               # 处理单个指令
    python main_qwen3.py -i                      # 交互模式
    python main_qwen3.py -f test_queries.txt     # 批量测试
    python main_qwen3.py --stats                 # 显示引擎统计信息
    python main_qwen3.py --config ollama        # 使用 Ollama 配置
"""

import sys
import argparse
import json
from pathlib import Path
from typing import List

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.hybrid.inference_engine_v3 import InferenceEngineV3, InferenceResult
from config.engine_config import EngineConfig, apply_template, CONFIG_TEMPLATES


# ==================== 引擎初始化 ====================

_engine_instance = None


# 全局变量记录引擎初始化时间
_engine_init_time = None


def get_engine(config: EngineConfig = None) -> InferenceEngineV3:
    """获取引擎实例（单例模式）"""
    global _engine_instance, _engine_init_time
    if _engine_instance is None:
        import time
        print("[初始化引擎]")
        print("正在加载推理引擎 V3...")
        start = time.perf_counter()

        # 如果没有提供配置，使用默认配置
        if config is None:
            config = EngineConfig()

        _engine_instance = InferenceEngineV3(
            router_model_path="data/models/router_clean_final/best_model.pth",
            skills_dir=None,
            use_llm=config.is_llm_enabled(),
            use_embedding=True,
            retriever_device="cuda",
            device="cuda",
            execute_skills=True,
            use_mock_api=True,
            llm_config=config
        )

        _engine_init_time = time.perf_counter() - start
        print(f"\n[OK] 引擎加载完成 (耗时: {_engine_init_time:.2f}秒)")
        print(f"LLM 配置: {config.get_provider_info()}")
    return _engine_instance


# ==================== 结果展示 ====================

def print_header(text: str, width: int = 70):
    """打印标题"""
    print("\n" + "=" * width)
    print(text.center(width))
    print("=" * width)


def print_stage(num: int, name: str, status: str = "OK"):
    """打印阶段标题"""
    icon = "[OK]" if status == "OK" else "[?]" if status == "?" else "[X]"
    print(f"\n{icon} [第{num}步] {name}")


def display_result(result: InferenceResult, show_details: bool = True, config: EngineConfig = None):
    """显示完整的推理结果"""

    print_header("处理结果")

    # 用户输入
    print(f"\n用户输入: {result.user_input}")

    # 显示时间统计说明
    if _engine_init_time:
        print(f"\n[时间统计]")
        print(f"  引擎初始化: {_engine_init_time:.2f}秒 (仅首次)")
        print(f"  指令处理: {result.latency_ms:.2f}ms")
        print(f"  总耗时(首次): {_engine_init_time * 1000 + result.latency_ms:.2f}ms")
        print(f"  总耗时(后续): {result.latency_ms:.2f}ms")

    # 显示 LLM 配置
    if config:
        print(f"\n[LLM 配置]")
        print(f"  提供商: {config.get_provider_info()}")
        print(f"  模型: {config.llm_config.model_name}")

    # 第1步：路由分类
    print_stage(1, "路由分类", "OK" if result.category else "?")
    if result.category:
        print(f"  分类结果: {result.category}")
        print(f"  预估延迟: ~1ms")
    else:
        print(f"  分类结果: 未知")

    # 第2步：技能检索
    if result.processing_path.value == "retrieval":
        print_stage(2, "技能检索 (混合检索)", "OK")
        if 'keyword_score' in result.metadata:
            print(f"  关键词分数: {result.metadata['keyword_score']:.3f}")
            print(f"  向量分数: {result.metadata['vector_score']:.3f}")
        print(f"  预估延迟: ~2.5ms")
    elif result.processing_path.value == "direct":
        print_stage(2, "直接执行", "OK")
        print(f"  预估延迟: ~1ms")
    else:
        print_stage(2, "技能检索", "?")
        print(f"  未执行检索")

    # 第3步：LLM解析
    print_stage(3, "LLM解析", "OK" if result.skill_id else "?")
    if result.skill_id:
        print(f"  技能ID: {result.skill_id}")
        print(f"  技能名称: {result.skill_name}")
        print(f"  参数: {result.parameters}")
        print(f"  置信度: {result.confidence:.3f}")
        print(f"  预估延迟: ~0.5ms")
    else:
        print(f"  未匹配到技能")

    # 第4步：技能执行
    if result.execution_result:
        status = "OK" if result.execution_result.status == 'success' else "X"
        print_stage(4, f"技能执行", status)
        print(f"  API: {result.execution_result.api_called}")
        print(f"  参数: {result.execution_result.api_params}")
        print(f"  执行延迟: {result.execution_result.latency_ms:.2f}ms")
        print(f"  响应: {result.execution_result.message}")
    else:
        print_stage(4, "技能执行", "?")
        print(f"  未执行")

    # 第5步：输出结果
    print_stage(5, "输出结果", "OK" if not result.needs_clarification else "?")
    print(f"  响应: {result.explanation}")
    if result.needs_clarification:
        print(f"  状态: 需要追问用户")

    # 总延迟
    print(f"\n总延迟: {result.latency_ms:.2f}ms")
    print(f"处理路径: {result.processing_path.value}")


def display_simple_result(result: InferenceResult, config: EngineConfig = None):
    """显示简化版结果（适合批量模式）"""
    status = "[OK]" if not result.needs_clarification else "[?]"
    exec_status = "[OK]" if result.execution_result and result.execution_result.status == 'success' else "[X]"

    print(f"\n{status} {result.user_input}")
    print(f"   LLM: {config.get_provider_info() if config else '规则引擎'}")
    print(f"   路由: {result.category or '未知'}")
    print(f"   路径: {result.processing_path.value}")

    if result.skill_id:
        print(f"   技能: {result.skill_name} ({result.confidence:.2f})")
        print(f"   执行: {exec_status} {result.execution_result.message if result.execution_result else '未执行'}")
    else:
        print(f"   说明: {result.explanation}")

    print(f"   延迟: {result.latency_ms:.2f}ms")


# ==================== 命令处理 ====================

def process_query(query: str, user_id: str = "cli_user", verbose: bool = True, config: EngineConfig = None):
    """处理单个查询"""
    engine = get_engine(config)

    result = engine.process(query, user_id)

    if verbose:
        display_result(result, verbose, config)
    else:
        display_simple_result(result, config)

    return result


def process_interactive(config: EngineConfig = None):
    """交互模式"""
    print_header("车控技能推理引擎 - 交互模式")

    engine = get_engine(config)

    stats = engine.get_stats()
    print(f"\n[引擎信息]")
    print(f"  技能总数: {stats['total_skills']}")
    print(f"  类别数: {len(stats['categories'])}")
    print(f"  流程完整度: 100% (6/6阶段)")
    print(f"  LLM 配置: {config.get_provider_info() if config else '规则引擎'}")

    print("\n" + "=" * 70)
    print("输入指令进行测试，输入 'quit' 或 'exit' 退出")
    print("输入 'switch config' 切换 LLM 配置")
    print("=" * 70)

    user_id = "interactive_user"

    while True:
        try:
            query = input("\n>>> ").strip()

            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n再见！")
                break

            # 切换配置
            if query.lower() == 'switch config':
                print("\n可用配置模板:")
                for name in CONFIG_TEMPLATES:
                    print(f"  {name}: {CONFIG_TEMPLATES[name]['provider']}")

                template_name = input("\n请选择配置模板 (或回车取消): ").strip()
                if template_name in CONFIG_TEMPLATES:
                    apply_template(template_name)
                    config = EngineConfig()
                    engine.update_llm_config(config)
                    print(f"已切换到: {config.get_provider_info()}")
                continue

            result = engine.process(query, user_id)
            display_result(result, True, config)

            # 显示历史
            history = engine.get_history(user_id)
            if len(history) > 1:
                print(f"\n[对话历史] (最近{len(history)}轮)")
                for i, h in enumerate(history[-5:], 1):
                    print(f"  {i}. {h.user_input}")

        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()


def process_batch(queries: List[str], verbose: bool = False, config: EngineConfig = None):
    """批量处理"""
    print_header("批量处理模式")

    engine = get_engine(config)

    print(f"\n[批量处理]")
    print(f"  查询数: {len(queries)}")
    print(f"  LLM配置: {config.get_provider_info() if config else '规则引擎'}")

    results = []
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] {query}")
        result = engine.process(query, "batch_user")
        results.append(result)

        if verbose:
            display_result(result, True, config)
        else:
            display_simple_result(result, config)

    # 统计
    success = sum(1 for r in results if not r.needs_clarification)
    executed = sum(1 for r in results if r.execution_result and r.execution_result.status == 'success')

    print_header("批量处理统计")
    print(f"\n总样本: {len(results)}")
    print(f"处理成功: {success} ({success/len(results)*100:.1f}%)")
    print(f"执行成功: {executed} ({executed/len(results)*100:.1f}%)")


def process_file(file_path: str, verbose: bool = False, config: EngineConfig = None):
    """从文件读取查询并处理"""
    path = Path(file_path)

    if not path.exists():
        print(f"错误: 文件不存在: {file_path}")
        return

    # 读取文件
    if path.suffix == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                queries = [item.get('text', item) if isinstance(item, dict) else item for item in data]
            else:
                queries = [data.get('query', '')]
    else:
        with open(path, 'r', encoding='utf-8') as f:
            queries = [line.strip() for line in f if line.strip()]

    process_batch(queries, verbose, config)


def show_stats(config: EngineConfig = None):
    """显示引擎统计信息"""
    print_header("引擎统计信息")

    engine = get_engine(config)
    stats = engine.get_stats()

    print(f"\n[配置信息]")
    print(f"  路由模型: TextCNN (187K参数)")
    print(f"  设备: {stats['device']}")
    print(f"  检索器: {stats['retriever_type']}")
    print(f"  向量检索: {'启用' if stats['use_embedding'] else '禁用'}")
    print(f"  LLM解析: {config.get_provider_info() if config else '规则引擎'}")
    print(f"  技能执行: {'启用' if stats['execute_skills'] else '禁用'}")

    print(f"\n[技能库]")
    print(f"  总技能数: {stats['total_skills']}")
    print(f"  类别数: {len(stats['categories'])}")

    print(f"\n[类别分布]")
    categories = stats['categories']
    if isinstance(categories, list):
        for cat in sorted(categories):
            print(f"  {cat}")
    elif isinstance(categories, dict):
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}个技能")

    # 显示 LLM 详细配置
    if config and config.is_llm_enabled():
        print(f"\n[LLM 配置详情]")
        llm = config.llm_config
        print(f"  提供商: {llm.provider}")
        print(f"  模型: {llm.model_name}")
        if llm.provider == "ollama":
            print(f"  地址: {llm.base_url}")
        elif llm.provider == "api":
            print(f"  API提供商: {llm.api_provider}")
        print(f"  温度: {llm.temperature}")
        print(f"  最大token: {llm.max_tokens}")


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description="车控技能推理引擎 V3 - 支持 Qwen3-1.7B",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main_qwen3.py "打开空调"              # 处理单个指令（详细模式）
  python main_qwen3.py "打开空调" -s          # 处理单个指令（简化模式）
  python main_qwen3.py -i                     # 交互模式
  python main_qwen3.py -i --config ollama    # 交互模式（使用Ollama）
  python main_qwen3.py -f queries.txt         # 从文件读取查询
  python main_qwen3.py --stats                # 显示统计信息
  python main_qwen3.py --config-list          # 列出可用配置
        """
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="要处理的用户指令"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="交互模式"
    )

    parser.add_argument(
        "-f", "--file",
        help="从文件读取查询"
    )

    parser.add_argument(
        "-s", "--simple",
        action="store_true",
        help="简化输出格式"
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="显示引擎统计信息"
    )

    parser.add_argument(
        "--config",
        choices=CONFIG_TEMPLATES.keys(),
        help="使用预定义配置模板"
    )

    parser.add_argument(
        "--config-file",
        help="指定配置文件路径"
    )

    parser.add_argument(
        "--device",
        default="cuda",
        choices=["cuda", "cpu"],
        help="运行设备 (默认: cuda)"
    )

    parser.add_argument(
        "--config-list",
        action="store_true",
        help="列出所有可用配置模板"
    )

    args = parser.parse_args()

    # 显示配置列表
    if args.config_list:
        print_header("可用配置模板")
        for name, config in CONFIG_TEMPLATES.items():
            print(f"\n{name}:")
            print(f"  提供商: {config['provider']}")
            print(f"  模型: {config.get('model_name', 'N/A')}")
        return

    # 加载配置
    config = None
    if args.config:
        config = apply_template(args.config, args.config_file)
    elif args.config_file:
        config = EngineConfig(args.config_file)

    # 显示统计信息
    if args.stats:
        show_stats(config)
        return

    # 交互模式
    if args.interactive:
        process_interactive(config)
        return

    # 从文件读取
    if args.file:
        process_file(args.file, verbose=not args.simple, config=config)
        return

    # 处理单个查询
    if args.query:
        process_query(args.query, verbose=not args.simple, config=config)
        return

    # 没有参数，显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()