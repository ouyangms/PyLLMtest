"""
端到端推理引擎 V3 - 完整闭环版本
整合路由、检索、LLM解析、技能执行的完整流程
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import deque

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig
from src.router.contextual_dialog import ContextualDialogRouter
from src.hybrid.architecture import (
    HybridArchitectureConfig, DecisionLogic,
    ProcessingPath, RouterResult, FinalDecision
)
from src.hybrid.hybrid_retriever import HybridRetriever
from src.hybrid.llm_parser import LLMParser
from src.hybrid.skill_executor import SkillExecutor, ExecutionResult


@dataclass
class InferenceResult:
    """推理结果（完整版）"""
    user_input: str
    processing_path: ProcessingPath
    category: Optional[str]
    skill_id: Optional[str]
    skill_name: Optional[str]
    parameters: Dict[str, Any]
    confidence: float
    explanation: str
    needs_clarification: bool
    latency_ms: float
    metadata: Dict[str, Any]

    # 新增：执行结果
    execution_result: Optional[ExecutionResult] = None


class InferenceEngineV3:
    """端到端推理引擎 V3 - 完整闭环"""

    def __init__(
        self,
        router_model_path: str = "data/models/router_clean_final/best_model.pth",
        skills_dir: Path = None,
        use_llm: bool = False,
        use_embedding: bool = True,
        retriever_device: str = "auto",
        device: str = "cuda",
        execute_skills: bool = True,
        use_mock_api: bool = True
    ):
        """
        初始化推理引擎 V3

        Args:
            router_model_path: 路由模型路径
            skills_dir: 技能目录
            use_llm: 是否使用LLM
            use_embedding: 是否使用向量检索
            retriever_device: 检索器设备
            device: 路由模型设备
            execute_skills: 是否执行技能（新增）
            use_mock_api: 是否使用模拟API（新增）
        """
        print("=" * 70)
        print("初始化端到端推理引擎 V3 (完整闭环)")
        print("=" * 70)

        self.device = device
        self.use_llm = use_llm
        self.use_embedding = use_embedding
        self.execute_skills = execute_skills
        self.config = HybridArchitectureConfig()

        # 1. 初始化路由器
        print("\n[1/5] 加载路由模型...")
        self.router = ContextualDialogRouter(router_model_path, device)
        print("     [OK] 路由模型加载完成")

        # 2. 初始化混合检索器
        if skills_dir is None:
            skills_dir = Path("E:/ai/py/whisperModel/vc/skills")

        print(f"\n[2/5] 加载混合检索器...")
        print(f"     向量检索: {'启用' if use_embedding else '禁用'}")
        print(f"     检索设备: {retriever_device}")

        self.skill_retriever = HybridRetriever(
            skills_dir,
            use_embedding=use_embedding,
            device=retriever_device
        )
        print(f"     [OK] 加载 {self.skill_retriever.get_all_skills_count()} 个技能")

        # 3. 初始化LLM解析器
        print(f"\n[3/5] 初始化LLM解析器...")
        if use_llm:
            self.llm_parser = LLMParser(use_local_llm=False)
            print("     [OK] LLM解析器加载完成")
        else:
            self.llm_parser = None
            print("     [OK] 使用规则引擎")

        # 4. 初始化技能执行器（新增）
        if execute_skills:
            print(f"\n[4/5] 初始化技能执行器...")
            print(f"     执行技能: {'启用' if execute_skills else '禁用'}")
            print(f"     API模式: {'模拟' if use_mock_api else '真实'}")

            self.skill_executor = SkillExecutor(
                skills_dir,
                use_mock_api=use_mock_api
            )
            print("     [OK] 技能执行器加载完成")
        else:
            self.skill_executor = None

        # 5. 对话历史
        self.conversation_histories: Dict[str, deque] = {}

        print("\n" + "=" * 70)
        print("推理引擎 V3 初始化完成")
        print("=" * 70)
        print(f"配置:")
        print(f"  - 路由模型: TextCNN (设备: {device})")
        print(f"  - 检索器: 混合检索 (关键词+向量)")
        print(f"  - 向量检索: {'启用' if use_embedding else '禁用'}")
        print(f"  - LLM解析: {'启用' if use_llm else '规则引擎'}")
        print(f"  - 技能执行: {'启用' if execute_skills else '禁用'}")
        print("=" * 70)

    def _get_user_history(self, user_id: str) -> deque:
        """获取用户对话历史"""
        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = deque(maxlen=5)
        return self.conversation_histories[user_id]

    def _is_fuzzy_input(self, text: str) -> bool:
        """检测模糊输入"""
        fuzzy_patterns = [
            "调一调", "弄一下", "搞一下", "再弄一次",
            "恢复默认", "重置",
            "高点", "低点", "大点", "小点"
        ]

        for pattern in fuzzy_patterns:
            if pattern in text:
                return True

        return len(text) <= 2

    def _handle_multi_turn(
        self,
        user_input: str,
        user_id: str
    ) -> InferenceResult:
        """处理多轮对话"""
        history = self._get_user_history(user_id)

        # 尝试结合上下文
        if history:
            last_turn = history[-1]
            last_input = last_turn.metadata.get('original_input', '')

            # 上下文组合
            combined = self._combine_with_context(user_input, last_input)

            # 使用组合后的输入重新路由
            return self._process_input(combined, user_id, original_input=user_input, used_context=True)

        # 无历史，追问
        return InferenceResult(
            user_input=user_input,
            processing_path=ProcessingPath.MULTI_TURN,
            category=None,
            skill_id=None,
            skill_name=None,
            parameters={},
            confidence=0.0,
            explanation="输入模糊，请问您想控制什么？比如：空调、座椅、车窗？",
            needs_clarification=True,
            latency_ms=0.0,
            metadata={'original_input': user_input},
            execution_result=None
        )

    def _combine_with_context(self, current: str, previous: str) -> str:
        """结合上下文"""
        if current in ["温度", "风量"]:
            return f"空调{current}"
        elif current in ["加热", "通风"]:
            return f"座椅{current}"
        elif current in ["开", "关"]:
            return f"{previous}{current}"
        else:
            return current

    def _process_input(
        self,
        text: str,
        user_id: str,
        original_input: Optional[str] = None,
        used_context: bool = False
    ) -> InferenceResult:
        """处理输入（内部方法）"""
        start_time = time.perf_counter()

        # 1. 路由分类
        router_result = self.router.process_input(text, user_id)
        category = router_result['category']
        confidence = router_result['confidence']

        # 2. 决策处理路径
        processing_path = DecisionLogic.determine_processing_path(
            RouterResult(
                category=category,
                confidence=confidence,
                processing_path=ProcessingPath.DIRECT,
                metadata={'text': text}
            ),
            self._is_fuzzy_input(text)
        )

        # 3. 根据路径处理
        if processing_path == ProcessingPath.DIRECT:
            # 直接执行（简单指令）
            result = InferenceResult(
                user_input=original_input or text,
                processing_path=processing_path,
                category=category,
                skill_id=category,
                skill_name=f"{category}_direct",
                parameters={'action': text},
                confidence=confidence,
                explanation=f"直接执行{category}指令",
                needs_clarification=False,
                latency_ms=(time.perf_counter() - start_time) * 1000,
                metadata={'used_context': used_context},
                execution_result=None
            )

            # 如果启用技能执行，执行技能
            if self.execute_skills and self.skill_executor:
                execution_result = self._execute_skill_direct(
                    category,
                    result.parameters,
                    user_id
                )
                result.execution_result = execution_result

        elif processing_path == ProcessingPath.RETRIEVAL:
            # 混合检索
            candidates = self.skill_retriever.retrieve(
                query=text,
                category=category,
                top_k=3
            )

            if candidates and candidates[0]['similarity'] > 0.3:
                # 使用候选技能
                best_candidate = candidates[0]

                # 解析参数
                if self.llm_parser:
                    parse_result = self.llm_parser.parse_intent(
                        text,
                        candidates,
                        {'category': category}
                    )
                    skill_id = parse_result.skill_id
                    skill_name = parse_result.skill_name
                    parameters = parse_result.parameters
                    explanation = parse_result.reasoning
                else:
                    skill_id = best_candidate['skill_id']
                    skill_name = best_candidate['name']
                    parameters = {}
                    explanation = f"找到技能: {skill_name}"

                # 执行技能（新增）
                execution_result = None
                if self.execute_skills and self.skill_executor:
                    execution_result = self._execute_skill(
                        skill_id,
                        parameters,
                        user_id
                    )

                # 更新说明（包含执行结果）
                if execution_result:
                    if execution_result.status == 'success':
                        explanation = f"{explanation}，{execution_result.message}"
                    else:
                        explanation = f"{explanation}，{execution_result.message}"

                result = InferenceResult(
                    user_input=original_input or text,
                    processing_path=processing_path,
                    category=category,
                    skill_id=skill_id,
                    skill_name=skill_name,
                    parameters=parameters,
                    confidence=best_candidate['similarity'],
                    explanation=explanation,
                    needs_clarification=best_candidate['similarity'] < 0.5,
                    latency_ms=(time.perf_counter() - start_time) * 1000,
                    metadata={
                        'candidates': candidates,
                        'used_context': used_context,
                        'keyword_score': best_candidate.get('keyword_score', 0),
                        'vector_score': best_candidate.get('vector_score', 0)
                    },
                    execution_result=execution_result
                )
            else:
                # 未找到技能，使用LLM回退
                result = InferenceResult(
                    user_input=original_input or text,
                    processing_path=ProcessingPath.LLM_FALLBACK,
                    category=category,
                    skill_id=None,
                    skill_name=None,
                    parameters={},
                    confidence=0.0,
                    explanation=f"未找到匹配的{category}技能",
                    needs_clarification=True,
                    latency_ms=(time.perf_counter() - start_time) * 1000,
                    metadata={'used_context': used_context},
                    execution_result=None
                )

        elif processing_path == ProcessingPath.LLM_FALLBACK:
            # LLM回退
            result = InferenceResult(
                user_input=original_input or text,
                processing_path=processing_path,
                category=None,
                skill_id=None,
                skill_name=None,
                parameters={},
                confidence=0.0,
                explanation="未能识别意图，请重新表达",
                needs_clarification=True,
                latency_ms=(time.perf_counter() - start_time) * 1000,
                metadata={'used_context': used_context},
                execution_result=None
            )

        else:  # MULTI_TURN
            result = InferenceResult(
                user_input=original_input or text,
                processing_path=processing_path,
                category=None,
                skill_id=None,
                skill_name=None,
                parameters={},
                confidence=0.0,
                explanation="输入模糊，需要追问",
                needs_clarification=True,
                latency_ms=(time.perf_counter() - start_time) * 1000,
                metadata={'used_context': used_context},
                execution_result=None
            )

        # 保存到历史
        self._get_user_history(user_id).append(result)

        return result

    def _execute_skill_direct(
        self,
        category: str,
        parameters: Dict,
        user_id: str
    ) -> Optional[ExecutionResult]:
        """直接执行技能（用于DIRECT路径）"""
        try:
            # 将类别转换为技能ID
            skill_id_map = {
                "climate_control": "OpenAirConditionerMode",
                "seat_control": "SeatHeat",
                "music_media": "PlayMusic",
                # ... 更多映射
            }

            skill_id = skill_id_map.get(category, f"{category}_default")

            # 执行技能
            return self.skill_executor.execute(skill_id, parameters, user_id)

        except Exception as e:
            print(f"直接执行失败: {e}")
            return None

    def _execute_skill(
        self,
        skill_id: str,
        parameters: Dict,
        user_id: str
    ) -> Optional[ExecutionResult]:
        """执行技能"""
        try:
            return self.skill_executor.execute(skill_id, parameters, user_id)
        except Exception as e:
            print(f"技能执行失败: {e}")
            return None

    def process(
        self,
        user_input: str,
        user_id: str = "default"
    ) -> InferenceResult:
        """
        处理用户输入（主接口）

        Args:
            user_input: 用户输入
            user_id: 用户ID

        Returns:
            推理结果（包含执行结果）
        """
        # 检查模糊输入
        if self._is_fuzzy_input(user_input):
            return self._handle_multi_turn(user_input, user_id)

        # 正常处理流程
        return self._process_input(user_input, user_id)

    def clear_history(self, user_id: str = "default"):
        """清除用户历史"""
        if user_id in self.conversation_histories:
            self.conversation_histories[user_id].clear()

    def get_history(self, user_id: str = "default") -> List[InferenceResult]:
        """获取用户历史"""
        return list(self._get_user_history(user_id))

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息"""
        stats = {
            'total_skills': self.skill_retriever.get_all_skills_count(),
            'categories': self.skill_retriever.get_categories(),
            'device': self.device,
            'use_llm': self.use_llm,
            'use_embedding': self.use_embedding,
            'execute_skills': self.execute_skills,
            'retriever_type': 'HybridRetriever (关键词+向量)',
        }

        if self.skill_executor:
            stats['executor_api_mode'] = '模拟' if self.skill_executor.api_client.mock_mode else '真实'

        return stats


def demo_inference_engine_v3():
    """演示推理引擎 V3 - 完整闭环"""
    print("=" * 70)
    print("端到端推理引擎 V3 演示 - 完整闭环")
    print("=" * 70)

    # 初始化引擎
    engine = InferenceEngineV3(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        use_embedding=True,
        retriever_device="cuda",
        device="cuda",
        execute_skills=True,  # 启用技能执行
        use_mock_api=True     # 使用模拟API
    )

    # 显示引擎信息
    stats = engine.get_stats()
    print(f"\n引擎信息:")
    print(f"  技能总数: {stats['total_skills']}")
    print(f"  类别数: {len(stats['categories'])}")
    print(f"  设备: {stats['device']}")
    print(f"  检索器: {stats['retriever_type']}")
    print(f"  技能执行: {stats['execute_skills']}")
    print(f"  API模式: {stats.get('executor_api_mode', 'N/A')}")

    # 测试用例
    test_inputs = [
        "打开空调",           # 直接执行
        "温度24度",          # 检索+执行
        "座椅加热",           # 检索+执行
        "调大音量",           # 检索+执行
        "导航到公司",         # 检索+执行
        "调一调",             # 模糊输入
    ]

    print("\n" + "=" * 70)
    print("完整流程测试")
    print("=" * 70)

    user_id = "demo_user"

    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{'='*70}")
        print(f"[测试 {i}] {user_input}")
        print(f"{'='*70}")

        result = engine.process(user_input, user_id)

        # 显示完整结果
        print(f"处理路径: {result.processing_path.value}")
        print(f"类别: {result.category}")
        print(f"技能: {result.skill_name}")
        print(f"参数: {result.parameters}")
        print(f"置信度: {result.confidence:.2f}")
        print(f"说明: {result.explanation}")

        if result.needs_clarification:
            print(f"[需要追问]")

        # 显示执行结果（新增）
        if result.execution_result:
            exec_result = result.execution_result
            print(f"\n[执行结果]")
            print(f"  技能ID: {exec_result.skill_id}")
            print(f"  执行ID: {exec_result.execution_id}")
            print(f"  状态: {exec_result.status}")
            print(f"  消息: {exec_result.message}")
            print(f"  延迟: {exec_result.latency_ms:.2f} ms")
            if exec_result.error:
                print(f"  错误: {exec_result.error}")

        # 显示总延迟
        print(f"\n总延迟: {result.latency_ms:.2f} ms")

        # 显示检索分数
        if 'keyword_score' in result.metadata:
            print(f"检索分数: 关键词={result.metadata['keyword_score']:.2f}, "
                  f"向量={result.metadata['vector_score']:.2f}")

    print("\n" + "=" * 70)
    print("演示完成 - 完整流程已闭环！")
    print("=" * 70)


if __name__ == "__main__":
    demo_inference_engine_v3()
