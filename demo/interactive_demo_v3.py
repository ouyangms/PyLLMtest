"""
交互式演示 - 推理引擎V3
手动输入query，查看完整的6阶段处理流程
"""

import sys
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.inference_engine_v3 import InferenceEngineV3


def print_header(text: str, width: int = 70):
    """打印标题"""
    print("\n" + "=" * width)
    print(text.center(width))
    print("=" * width)


def print_section(text: str, width: int = 70):
    """打印小节标题"""
    print("\n" + "-" * width)
    print(text)
    print("-" * width)


def display_result(result, engine, show_details: bool = True):
    """显示推理结果"""

    print(f"\n[处理结果]")
    print(f"  用户输入: {result.user_input}")
    print(f"  处理路径: {result.processing_path.value}")

    if result.category:
        print(f"  路由类别: {result.category}")

    if result.skill_id:
        print(f"  匹配技能: {result.skill_name}")
        print(f"  技能ID: {result.skill_id}")
        print(f"  参数: {result.parameters}")
        print(f"  置信度: {result.confidence:.3f}")

    if result.execution_result:
        exec_result = result.execution_result
        status_icon = "[OK]" if exec_result.status == 'success' else "[X]"
        print(f"\n[执行结果] {status_icon}")
        print(f"  技能ID: {exec_result.skill_id}")
        print(f"  执行ID: {exec_result.execution_id}")
        print(f"  状态: {exec_result.status}")
        print(f"  消息: {exec_result.message}")
        print(f"  执行延迟: {exec_result.latency_ms:.2f} ms")

        if show_details:
            print(f"\n[API详情]")
            print(f"  API: {exec_result.api_called}")
            print(f"  参数: {exec_result.api_params}")

    print(f"\n[响应]")
    print(f"  {result.explanation}")

    if result.needs_clarification:
        print(f"  [需要追问用户]")

    print(f"\n[性能]")
    print(f"  总延迟: {result.latency_ms:.2f} ms")

    if show_details and 'keyword_score' in result.metadata:
        print(f"  检索分数: 关键词={result.metadata['keyword_score']:.2f}, "
              f"向量={result.metadata['vector_score']:.2f}")


def show_pipeline_diagram():
    """显示流程图"""
    print("""
    ┌─────────────────────────────────────────────────────────────┐
    │                    完整6阶段流程                            │
    └─────────────────────────────────────────────────────────────┘

    用户输入 "打开空调"
         │
         ▼
    ┌───────────────────────────────────────────────────────────┐
    │ 第1步: 路由分类 (TextCNN)                                 │
    │   输入: "打开空调"                                         │
    │   输出: climate_control (置信度: 0.95)                    │
    │   延迟: ~1ms                                              │
    └───────────────────────────────────────────────────────────┘
         │
         ▼
    ┌───────────────────────────────────────────────────────────┐
    │ 第2步: 技能检索 (混合检索)                                │
    │   输入: climate_control + "打开空调"                      │
    │   检索: 关键词(0.3) + 向量(0.7)                           │
    │   输出: Top-3 候选技能                                    │
    │   延迟: ~2.5ms                                            │
    └───────────────────────────────────────────────────────────┘
         │
         ▼
    ┌───────────────────────────────────────────────────────────┐
    │ 第3步: LLM解析 (规则引擎)                                 │
    │   输入: 用户查询 + 候选技能                               │
    │   输出: skill_id + parameters                             │
    │   延迟: ~0.5ms                                            │
    └───────────────────────────────────────────────────────────┘
         │
         ▼
    ┌───────────────────────────────────────────────────────────┐
    │ 第4步: 技能执行 (SkillExecutor)                           │
    │   输入: OpenAirConditionerMode + {"action": "open"}       │
    │   API: sys.car.crl                                        │
    │   输出: 执行结果                                          │
    │   延迟: ~10ms                                             │
    └───────────────────────────────────────────────────────────┘
         │
         ▼
    ┌───────────────────────────────────────────────────────────┐
    │ 第5步: 输出结果                                           │
    │   "空调已打开"                                            │
    └───────────────────────────────────────────────────────────┘
    """)


def interactive_demo():
    """交互式演示"""

    print_header("推理引擎V3 - 交互式演示")

    # 初始化引擎
    print("\n[初始化引擎]")
    print("正在加载推理引擎V3...")

    engine = InferenceEngineV3(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        use_embedding=True,
        retriever_device="cuda",
        device="cuda",
        execute_skills=True,
        use_mock_api=True
    )

    stats = engine.get_stats()
    print(f"\n[引擎信息]")
    print(f"  技能总数: {stats['total_skills']}")
    print(f"  设备: {stats['device']}")
    print(f"  流程完整度: 100% (6/6阶段)")

    # 显示流程图
    show_pipeline_diagram()

    # 推荐测试用例
    print("\n[推荐测试用例]")
    test_cases = [
        ("打开空调", "直接执行 - 空调控制"),
        ("温度24度", "检索+执行 - 温度调节"),
        ("座椅加热", "检索+执行 - 座椅控制"),
        ("调大音量", "检索+执行 - 音量控制"),
        ("导航到公司", "检索+执行 - 导航"),
        ("调一调", "多轮对话 - 模糊输入"),
    ]

    for i, (query, desc) in enumerate(test_cases, 1):
        print(f"  {i}. \"{query}\" - {desc}")

    print("\n" + "=" * 70)
    print("输入 'quit' 或 'exit' 退出")
    print("=" * 70)

    # 交互循环
    user_id = "demo_user"

    while True:
        print("\n" + "=" * 70)
        user_input = input("请输入指令: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ['quit', 'exit', '退出', 'q']:
            print("\n再见！")
            break

        # 处理输入
        print(f"\n[处理中...]")
        result = engine.process(user_input, user_id)

        # 显示结果
        display_result(result, engine, show_details=True)

        # 显示历史
        history = engine.get_history(user_id)
        if len(history) > 1:
            print(f"\n[对话历史] (最近{len(history)}轮)")
            for i, h in enumerate(history[-3:], 1):
                print(f"  {i}. {h.user_input} -> {h.processing_path.value}")


if __name__ == "__main__":
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
