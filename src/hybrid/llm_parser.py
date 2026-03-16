"""
LLM意图解析器
使用LLM进行复杂的意图理解和参数提取
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

sys.path.insert(0, 'E:/ai/py/whisperModel')


@dataclass
class ParsedResult:
    """解析结果"""
    skill_id: str
    skill_name: str
    parameters: Dict[str, Any]
    confidence: float
    reasoning: str


class LLMParser:
    """LLM意图解析器"""

    def __init__(
        self,
        use_local_llm: bool = False,
        model_path: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """
        初始化LLM解析器

        Args:
            use_local_llm: 是否使用本地LLM
            model_path: 本地LLM路径
            api_key: API密钥（如果使用云端LLM）
        """
        self.use_local_llm = use_local_llm
        self.model_path = model_path
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name

        if use_local_llm:
            self._init_local_llm()
        else:
            print("使用规则引擎（LLM未配置）")

    def _init_local_llm(self):
        """初始化本地LLM"""
        try:
            if self.base_url and "localhost" in self.base_url:
                # 使用Ollama
                import requests
                self._ollama_client = requests.Session()
                self._ollama_base_url = self.base_url
                self._ollama_model = self.model_name or "qwen3:1.7b"
                print(f"Ollama初始化成功: {self._ollama_model}")
            else:
                # 使用llama.cpp
                self._init_llama_cpp()
        except Exception as e:
            print(f"LLM初始化失败: {e}，使用规则引擎")
            self.use_local_llm = False

    def parse_intent(
        self,
        user_input: str,
        skill_candidates: List[Dict],
        context: Optional[Dict] = None
    ) -> ParsedResult:
        """
        解析用户意图

        Args:
            user_input: 用户输入
            skill_candidates: 技能候选列表
            context: 上下文信息

        Returns:
            解析结果
        """
        if not skill_candidates:
            return self._parse_with_rules(user_input, context)

        # 使用LLM或规则引擎
        if self.use_local_llm:
            return self._parse_with_llm(user_input, skill_candidates, context)
        else:
            return self._parse_with_rules(user_input, skill_candidates, context)

    def _parse_with_llm(
        self,
        user_input: str,
        skill_candidates: List[Dict],
        context: Optional[Dict] = None
    ) -> ParsedResult:
        """使用LLM解析意图"""
        # 构建提示词
        prompt = self._build_llm_prompt(user_input, skill_candidates, context)

        # 调用LLM（这里使用模拟响应）
        try:
            llm_response = self._call_llm(prompt)
            return self._parse_llm_response(llm_response)
        except Exception as e:
            print(f"LLM调用失败: {e}，使用规则引擎")
            return self._parse_with_rules(user_input, skill_candidates, context)

    def _build_llm_prompt(
        self,
        user_input: str,
        skill_candidates: List[Dict],
        context: Optional[Dict] = None
    ) -> str:
        """构建LLM提示词"""
        prompt = f"""你是一个车载语音助手的意图解析器。请根据用户输入和候选技能，解析出最匹配的技能和参数。

用户输入: {user_input}

候选技能:
"""

        for i, skill in enumerate(skill_candidates[:3], 1):
            prompt += f"\n{i}. 技能ID: {skill['skill_id']}\n"
            prompt += f"   名称: {skill['name']}\n"
            prompt += f"   描述: {skill['description']}\n"

        prompt += f"""
请以JSON格式返回解析结果，格式如下:
{{
    "skill_id": "最匹配的技能ID",
    "parameters": {{"参数名": "参数值"}},
    "confidence": 0.95,
    "reasoning": "选择该技能的原因"
}}

只返回JSON，不要有其他内容。"""

        return prompt

    def _call_llm(self, prompt: str) -> str:
        """调用LLM"""
        if hasattr(self, '_ollama_client'):
            # 使用Ollama
            return self._call_ollama(prompt)
        elif hasattr(self, '_llama_cpp'):
            # 使用llama.cpp
            return self._call_llama_cpp(prompt)
        else:
            # 模拟响应
            return self._get_mock_response()

    def _init_llama_cpp(self):
        """初始化llama.cpp"""
        try:
            import llama_cpp
            self._llama_cpp = llama_cpp.Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=4,
                n_batch=512,
                use_mmap=True,
                use_mlock=False
            )
            print(f"llama.cpp初始化成功: {self.model_path}")
        except Exception as e:
            raise Exception(f"llama.cpp初始化失败: {e}")

    def _call_ollama(self, prompt: str) -> str:
        """调用Ollama API"""
        try:
            data = {
                "model": self._ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1000
                }
            }

            response = self._ollama_client.post(
                f"{self._ollama_base_url}/api/generate",
                json=data,
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

            return result.get("response", "")
        except Exception as e:
            print(f"Ollama调用失败: {e}")
            return self._get_mock_response()

    def _call_llama_cpp(self, prompt: str) -> str:
        """调用llama.cpp"""
        try:
            response = self._llama_cpp(
                prompt,
                max_tokens=1000,
                temperature=0.7,
                stop=["\n\n", "JSON"],
                repeat_penalty=1.1
            )

            return response['choices'][0]['text']
        except Exception as e:
            print(f"llama.cpp调用失败: {e}")
            return self._get_mock_response()

    def _get_mock_response(self) -> str:
        """获取模拟响应"""
        return """
{
    "skill_id": "AdjustAirConditionerAbsoluteTemperature",
    "parameters": {"temperature": 24, "zone": "all"},
    "confidence": 0.92,
    "reasoning": "用户想调节空调温度，根据上下文推断为24度"
}
"""

    def _parse_llm_response(self, response: str) -> ParsedResult:
        """解析LLM响应"""
        try:
            result = json.loads(response)
            return ParsedResult(
                skill_id=result.get("skill_id", ""),
                skill_name=result.get("skill_id", ""),  # 需要从skill_id映射
                parameters=result.get("parameters", {}),
                confidence=result.get("confidence", 0.5),
                reasoning=result.get("reasoning", "")
            )
        except Exception as e:
            print(f"LLM响应解析失败: {e}")
            # 返回默认结果
            return ParsedResult(
                skill_id="",
                skill_name="",
                parameters={},
                confidence=0.0,
                reasoning="解析失败"
            )

    def _parse_with_rules(
        self,
        user_input: str,
        skill_candidates: List[Dict],
        context: Optional[Dict] = None
    ) -> ParsedResult:
        """使用规则引擎解析意图"""
        if not skill_candidates:
            return ParsedResult(
                skill_id="",
                skill_name="",
                parameters={},
                confidence=0.0,
                reasoning="未找到匹配的技能"
            )

        # 选择最佳匹配
        best_skill = skill_candidates[0]
        similarity = best_skill.get('similarity', 0.0)

        # 提取参数
        parameters = self._extract_parameters(user_input, best_skill)

        # 计算置信度
        confidence = min(similarity, 0.95)

        # 如果相似度高，置信度也高
        if similarity > 0.8:
            confidence = 0.95

        return ParsedResult(
            skill_id=best_skill['skill_id'],
            skill_name=best_skill['name'],
            parameters=parameters,
            confidence=confidence,
            reasoning=f"基于关键词匹配，相似度: {similarity:.2f}"
        )

    def _extract_parameters(self, user_input: str, skill: Dict) -> Dict[str, Any]:
        """从用户输入中提取参数"""
        parameters = {}
        params_schema = skill.get('params_schema', {})

        # 提取数字
        numbers = re.findall(r'\d+', user_input)
        if numbers and params_schema:
            # 尝试匹配数字参数
            for param_name, param_type in params_schema.items():
                if param_type == 'integer' and numbers:
                    parameters[param_name] = int(numbers[0])
                    break

        # 提取位置信息
        positions = {
            "左前": "front_left", "右前": "front_right",
            "左后": "rear_left", "右后": "rear_right",
            "主驾": "driver", "副驾": "passenger",
            "前": "front", "后": "rear", "全": "all"
        }
        for pos_zh, pos_en in positions.items():
            if pos_zh in user_input and 'position' in str(params_schema):
                parameters['position'] = pos_en
                break

        # 提取开关状态
        if any(word in user_input for word in ["打开", "开启", "启动"]):
            parameters['action'] = 'open'
        elif any(word in user_input for word in ["关闭", "停止"]):
            parameters['action'] = 'close'

        return parameters


class HybridLLMEngine:
    """混合LLM引擎（支持多种LLM后端）"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化混合引擎

        Args:
            config: 配置字典
                - use_local: 是否使用本地LLM
                - use_api: 是否使用API
                - model_path: 本地模型路径
                - api_key: API密钥
                - api_base: API地址
                - model_name: 模型名称
        """
        self.config = config
        self.parser = None

        if config.get('use_local', False):
            self.parser = LLMParser(
                use_local_llm=True,
                model_path=config.get('model_path'),
                api_key=config.get('api_key'),
                base_url=config.get('base_url'),
                model_name=config.get('model_name')
            )
        elif config.get('use_api', False):
            self.parser = LLMParser(
                use_local_llm=False,
                api_key=config.get('api_key'),
                model_name=config.get('model_name')
            )
        else:
            # 使用规则引擎
            self.parser = LLMParser(use_local_llm=False)

    def parse(
        self,
        user_input: str,
        skill_candidates: List[Dict],
        context: Optional[Dict] = None
    ) -> ParsedResult:
        """解析意图"""
        return self.parser.parse_intent(user_input, skill_candidates, context)

    def is_available(self) -> bool:
        """检查LLM是否可用"""
        return self.parser is not None


def test_llm_parser():
    """测试LLM解析器"""
    print("=" * 70)
    print("LLM意图解析器测试")
    print("=" * 70)

    # 创建解析器（使用规则引擎）
    parser = LLMParser(use_local_llm=False)

    # 模拟技能候选
    skill_candidates = [
        {
            'skill_id': 'OpenAC',
            'name': '打开空调',
            'description': '打开空调系统',
            'params_schema': {'action': 'string'},
            'similarity': 0.85
        },
        {
            'skill_id': 'SetTemperature',
            'name': '设置空调温度',
            'description': '设置空调到指定温度',
            'params_schema': {'temperature': 'integer', 'zone': 'string'},
            'similarity': 0.75
        }
    ]

    # 测试用例
    test_cases = [
        ("打开空调", skill_candidates, None),
        ("空调24度", skill_candidates, None),
        ("温度调高", skill_candidates, None),
    ]

    for user_input, candidates, context in test_cases:
        print(f"\n用户输入: {user_input}")

        result = parser.parse_intent(user_input, candidates, context)

        print(f"  技能ID: {result.skill_id}")
        print(f"  技能名称: {result.skill_name}")
        print(f"  参数: {result.parameters}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  推理: {result.reasoning}")


if __name__ == "__main__":
    test_llm_parser()
