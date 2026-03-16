"""
车控技能路由系统 - 混合架构设计
路由模型 + LLM 的三层架构
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


class ConfidenceLevel(Enum):
    """置信度级别"""
    HIGH = "high"          # >0.9: 直接执行
    MEDIUM = "medium"      # 0.7-0.9: 技能检索
    LOW = "low"            # <0.7: LLM处理
    UNKNOWN = "unknown"    # 无法分类


class ProcessingPath(Enum):
    """处理路径"""
    DIRECT = "direct"              # 直接执行（路由高置信度 + 简单指令）
    RETRIEVAL = "retrieval"        # 技能检索（路由中置信度）
    LLM_FALLBACK = "llm_fallback"  # LLM回退（路由低置信度）
    MULTI_TURN = "multi_turn"      # 多轮对话（模糊输入）


@dataclass
class RouterResult:
    """路由结果"""
    category: str
    confidence: float
    processing_path: ProcessingPath
    metadata: Dict[str, Any]


@dataclass
class SkillCandidate:
    """技能候选"""
    skill_id: str
    name: str
    description: str
    params_schema: Dict[str, Any]
    similarity: float


@dataclass
class LLMResult:
    """LLM处理结果"""
    skill_id: Optional[str]
    parameters: Dict[str, Any]
    confidence: float
    reasoning: str


@dataclass
class FinalDecision:
    """最终决策"""
    processing_path: ProcessingPath
    skill_id: str
    parameters: Dict[str, Any]
    confidence: float
    explanation: str
    needs_clarification: bool


class HybridArchitectureConfig:
    """混合架构配置"""

    # 模型配置
    MODELS = {
        "router": {
            "name": "Router",
            "path": "data/models/router_clean_final/best_model.pth",
            "type": "textcnn",
            "size": "<10MB",
            "quantization": "INT8"
        },
        "llm": {
            "name": "Qwen3-1.7B",
            "provider": "local",
            "deployment": "llama.cpp",
            "quantization": "Q4_K_M",
            "size": "~4-5GB",
            "ctx_length": 2048,
            "performance": {
                "latency": "<300ms",
                "memory": "~4-5GB"
            },
            "supports": ["grammar_constraint", "vulkan_gpu"]
        },
        "embedding": {
            "name": "bge-small-zh-v1.5",
            "type": "embedding",
            "dim": 384,
            "size": "~30MB"
        }
    }

    # 置信度阈值
    ROUTER_HIGH_CONFIDENCE = 0.90    # 路由高置信度阈值
    ROUTER_LOW_CONFIDENCE = 0.70     # 路由低置信度阈值

    # 技能检索配置
    RETRIEVAL_TOP_K = 3               # 检索Top-K技能
    RETRIEVAL_MIN_SIMILARITY = 0.5    # 最小相似度阈值

    # LLM配置
    LLM_FALLBACK_CONFIDENCE = 0.70   # LLM回退置信度阈值
    LLM_MAX_TOKENS = 512              # LLM最大tokens
    LLM_TEMPERATURE = 0.3             # LLM温度（低温度保证稳定性）

    # 多轮对话配置
    MAX_TURNS = 3                     # 最大对话轮数
    CLARIFICATION_TIMEOUT = 30        # 追问超时（秒）

    # 简单指令模式（直接执行）
    SIMPLE_PATTERNS = [
        "打开",
        "关闭",
        "启动",
        "停止",
        "是",
        "确认",
        "好的",
        "取消",
    ]


class DecisionLogic:
    """决策逻辑"""

    @staticmethod
    def determine_processing_path(
        router_result: RouterResult,
        is_fuzzy_input: bool = False
    ) -> ProcessingPath:
        """
        确定处理路径

        决策树：
        1. 模糊输入 → 多轮对话
        2. 路由高置信度 + 简单指令 → 直接执行
        3. 路由高置信度 → 技能检索
        4. 路由中置信度 → 技能检索
        5. 路由低置信度 → LLM回退
        """
        if is_fuzzy_input:
            return ProcessingPath.MULTI_TURN

        if router_result.confidence >= HybridArchitectureConfig.ROUTER_HIGH_CONFIDENCE:
            # 检查是否为简单指令
            if DecisionLogic._is_simple_command(router_result.metadata.get('text', '')):
                return ProcessingPath.DIRECT
            return ProcessingPath.RETRIEVAL

        if router_result.confidence >= HybridArchitectureConfig.ROUTER_LOW_CONFIDENCE:
            return ProcessingPath.RETRIEVAL

        return ProcessingPath.LLM_FALLBACK

    @staticmethod
    def _is_simple_command(text: str) -> bool:
        """判断是否为简单指令"""
        for pattern in HybridArchitectureConfig.SIMPLE_PATTERNS:
            if pattern in text and len(text) <= 10:
                return True
        return False

    @staticmethod
    def should_use_llm(
        skill_candidates: List[SkillCandidate],
        router_confidence: float
    ) -> bool:
        """
        判断是否应该使用LLM

        条件：
        1. 技能检索结果不足（<1个）
        2. 最高相似度低于阈值
        3. 路由置信度低
        """
        if len(skill_candidates) == 0:
            return True

        if skill_candidates[0].similarity < HybridArchitectureConfig.RETRIEVAL_MIN_SIMILARITY:
            return True

        if router_confidence < HybridArchitectureConfig.ROUTER_LOW_CONFIDENCE:
            return True

        return False


class DataFlow:
    """数据流定义"""

    @staticmethod
    def describe_flow() -> str:
        """描述完整数据流"""
        return """
        车控技能路由系统 - 数据流
        ==============================

        1. 用户输入
           ↓
        2. 预处理
           - 文本清洗
           - 模糊检测
           ↓
        3. 路由分类 (TextCNN)
           - 输入: 用户文本
           - 输出: 类别 + 置信度
           - 延迟: <1ms
           ↓
        4. 决策引擎
           ├─ 模糊输入 → 多轮对话
           ├─ 高置信度 + 简单指令 → 直接执行
           ├─ 高/中置信度 → 技能检索
           └─ 低置信度 → LLM回退
           ↓
        5. 技能检索 (FAISS/关键词)
           - 输入: 类别 + 用户文本
           - 输出: Top-K 技能候选
           - 延迟: <10ms
           ↓
        6. LLM解析 (可选)
           - 输入: 用户文本 + 技能候选
           - 输出: 技能ID + 参数
           - 延迟: <300ms
           ↓
        7. 执行引擎
           - 输入: 技能ID + 参数
           - 输出: 执行结果
           ↓
        8. 响应用户
        """

    @staticmethod
    def get_latency_budget() -> Dict[str, float]:
        """获取延迟预算（目标 <1s）"""
        return {
            "路由分类": 10,      # <10ms
            "技能检索": 50,      # <50ms
            "LLM解析": 300,      # <300ms (如果使用)
            "执行引擎": 100,     # <100ms
            "总计": 460,         # 目标 <1s
            "安全余量": 540      # 剩余时间
        }


class ArchitectureSpec:
    """架构规范"""

    def __init__(self):
        self.config = HybridArchitectureConfig()
        self.decision = DecisionLogic()
        self.data_flow = DataFlow()

    def get_specification(self) -> Dict[str, Any]:
        """获取完整架构规范"""
        return {
            "name": "车控技能路由系统",
            "version": "1.0",
            "architecture": "三层混合架构（路由 + 检索 + LLM）",
            "components": {
                "路由层": {
                    "model": "TextCNN",
                    "params": "187K",
                    "latency": "<1ms",
                    "accuracy": "99.51%",
                    "responsibility": "快速分类和简单指令处理"
                },
                "检索层": {
                    "method": "FAISS向量检索 + 关键词匹配",
                    "skills": "575个技能",
                    "latency": "<10ms",
                    "top_k": "3",
                    "responsibility": "从分类中检索相关技能"
                },
                "生成层": {
                    "model": "LLM (Qwen3-1.7B)",
                    "quantization": "Q4_K_M",
                    "latency": "<300ms",
                    "responsibility": "复杂意图理解和参数提取"
                }
            },
            "decision_logic": {
                "direct_execution": "路由高置信度 + 简单指令",
                "skill_retrieval": "路由中/高置信度",
                "llm_fallback": "路由低置信度",
                "multi_turn": "模糊输入"
            },
            "performance_targets": {
                "total_latency": "<1000ms",
                "accuracy": ">95%",
                "memory": "<3GB",
                "cpu_usage": "<80%"
            },
            "data_flow": self.data_flow.describe_flow(),
            "latency_budget": self.data_flow.get_latency_budget()
        }


def print_architecture_overview():
    """打印架构概览"""
    spec = ArchitectureSpec()
    spec_dict = spec.get_specification()

    print("=" * 70)
    print("车控技能路由系统 - 混合架构设计")
    print("=" * 70)

    print(f"\n版本: {spec_dict['version']}")
    print(f"架构: {spec_dict['architecture']}")

    print("\n组件:")
    print("-" * 70)
    for component, details in spec_dict['components'].items():
        print(f"\n{component}:")
        for key, value in details.items():
            print(f"  {key}: {value}")

    print("\n\n决策逻辑:")
    print("-" * 70)
    for logic, description in spec_dict['decision_logic'].items():
        print(f"  {logic}: {description}")

    print("\n\n性能目标:")
    print("-" * 70)
    for target, value in spec_dict['performance_targets'].items():
        print(f"  {target}: {value}")

    print("\n\n延迟预算:")
    print("-" * 70)
    for component, budget in spec_dict['latency_budget'].items():
        if component != "安全余量":
            print(f"  {component}: {budget}ms")
        else:
            print(f"  {component}: {budget}ms (总计: {sum(spec_dict['latency_budget'].values())}ms)")


if __name__ == "__main__":
    print_architecture_overview()
