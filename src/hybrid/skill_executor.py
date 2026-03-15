"""
技能执行器 - 调用车辆控制API
实现从技能ID到API调用的完整流程
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re

sys.path.insert(0, 'E:/ai/py/whisperModel')


@dataclass
class ExecutionResult:
    """执行结果"""
    skill_id: str
    execution_id: str
    status: str  # success, failed, pending
    message: str
    api_called: str
    api_params: Dict[str, Any]
    response_data: Dict[str, Any]
    error: Optional[str]
    latency_ms: float


class SkillDefinition:
    """技能定义"""

    def __init__(self, skill_id: str, name: str, description: str,
                 api: str, param_schema: Dict, examples: List[str],
                 param_template: Dict = None):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.api = api
        self.param_schema = param_schema
        self.examples = examples
        # 参数模板：从示例中提取的JSON格式
        self.param_template = param_template or {}

    @classmethod
    def from_file(cls, skill_id: str, skill_dir: Path) -> 'SkillDefinition':
        """从SKILL.md文件加载技能定义"""
        skill_file = skill_dir / skill_id / "SKILL.md"

        if not skill_file.exists():
            raise FileNotFoundError(f"技能文件不存在: {skill_file}")

        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析YAML frontmatter
        name = cls._extract_field(content, 'name')
        description = cls._extract_field(content, 'description')

        # 解析API信息（包含完整的api和param结构）
        api_info, param_template = cls._extract_api_info(content)

        # 解析参数规范
        param_schema = cls._extract_param_schema(content)

        # 解析示例
        examples = cls._extract_examples(content)

        return cls(
            skill_id=skill_id,
            name=name,
            description=description,
            api=api_info.get('api', ''),
            param_schema=param_schema,
            examples=examples,
            param_template=param_template
        )

    @staticmethod
    def _extract_field(content: str, field: str) -> str:
        """提取字段"""
        pattern = rf'{field}:\s*(.+?)(?=\n|$)'
        match = re.search(pattern, content)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_api_info(content: str):
        """提取API信息和参数模板"""
        api_info = {}
        param_template = {}

        # 查找所有的JSON示例
        json_pattern = r'```json\s*(\{[^`]+?\})\s*```'
        matches = re.findall(json_pattern, content, re.DOTALL)

        if matches:
            try:
                # 第一个示例通常是参数规范的示例
                first_example = json.loads(matches[0])

                # 提取API名称
                if 'api' in first_example:
                    api_info['api'] = first_example['api']

                # 提取参数模板（保留完整的param结构）
                if 'param' in first_example:
                    param_template = first_example['param'].copy()
            except Exception as e:
                print(f"  [警告] 解析API示例失败: {e}")

        return api_info, param_template

    @staticmethod
    def _extract_param_schema(content: str) -> Dict:
        """提取参数规范"""
        schema = {}

        # 查找参数说明表格
        lines = content.split('\n')
        in_param_section = False

        for line in lines:
            if '参数规范' in line or '参数说明' in line:
                in_param_section = True
                continue

            if in_param_section:
                if line.strip().startswith('|'):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 3 and parts[1] != '---':
                        param_name = parts[1]
                        param_type = parts[2] if len(parts) > 2 else ''
                        schema[param_name] = param_type
                elif line.strip().startswith('##'):
                    break

        return schema

    @staticmethod
    def _extract_examples(content: str) -> List[str]:
        """提取示例"""
        examples = []

        # 查找示例部分
        lines = content.split('\n')
        in_example = False
        current_example = []

        for line in lines:
            if '示例' in line and '用户输入' in line:
                in_example = True
                continue

            if in_example:
                if line.strip().startswith('```'):
                    if current_example:
                        examples.append('\n'.join(current_example))
                    current_example = []
                    in_example = False
                elif line.strip().startswith('**用户输入**'):
                    current_example.append(line.replace('**用户输入**:', '').strip())
                else:
                    current_example.append(line.strip())

        return examples


class VehicleAPIClient:
    """车辆控制API客户端（模拟版本）"""

    def __init__(self, mock_mode: bool = True):
        """
        初始化API客户端

        Args:
            mock_mode: 是否使用模拟模式
        """
        self.mock_mode = mock_mode
        self.auth_token = None

        if mock_mode:
            print("  [模拟模式] 车辆控制API客户端初始化")
        else:
            print("  [真实模式] 车辆控制API客户端初始化")

    def call(self, api: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用车辆控制API

        Args:
            api: API名称 (如 "sys.car.crl")
            params: API参数

        Returns:
            API响应
        """
        if self.mock_mode:
            return self._mock_call(api, params)
        else:
            return self._real_call(api, params)

    def _mock_call(self, api: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """模拟API调用"""
        # 模拟处理延迟
        time.sleep(0.01)

        # 根据API和参数生成模拟响应
        status = "success"
        message = "操作成功"

        # 根据不同的API类型生成响应
        if "crl" in api:
            # 空调相关API
            if params.get("part") == "温度":
                message = f"空调温度已设置为{params.get('value', '20')}度"
            elif params.get("action") == "open":
                message = "空调已打开"
            elif params.get("action") == "close":
                message = "空调已关闭"
            else:
                message = "空调控制指令已执行"

        elif "window" in api.lower():
            # 车窗控制
            if params.get("action") == "open":
                message = "车窗已打开"
            elif params.get("action") == "close":
                message = "车窗已关闭"
            else:
                message = "车窗控制指令已执行"

        elif "seat" in api.lower():
            # 座椅控制
            if params.get("part") == "加热":
                message = "座椅加热已开启"
            else:
                message = "座椅控制指令已执行"

        elif "music" in api.lower() or "audio" in api.lower():
            # 音乐媒体
            if "volume" in api.lower():
                message = f"音量已调至{params.get('value', '中')}"
            else:
                message = "媒体控制指令已执行"

        else:
            message = "车辆控制指令已执行"

        return {
            "status": status,
            "message": message,
            "data": {
                "execution_id": f"exec_{int(time.time()*1000)}",
                "timestamp": time.time(),
                "api": api,
                "params": params
            }
        }

    def _real_call(self, api: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """真实API调用（待实现）"""
        # TODO: 实现真实的HTTP调用
        # 1. 构建请求URL
        # 2. 添加认证头
        # 3. 发送POST请求
        # 4. 处理响应
        raise NotImplementedError("真实API调用尚未实现")


class SkillExecutor:
    """技能执行器 - 核心组件"""

    def __init__(self, skills_dir: Path, use_mock_api: bool = True):
        """
        初始化技能执行器

        Args:
            skills_dir: 技能目录
            use_mock_api: 是否使用模拟API
        """
        self.skills_dir = skills_dir
        self.skill_cache = {}  # 技能定义缓存

        # 初始化API客户端
        self.api_client = VehicleAPIClient(mock_mode=use_mock_api)

        print("技能执行器初始化完成")
        print(f"  技能目录: {skills_dir}")
        print(f"  API模式: {'模拟' if use_mock_api else '真实'}")

    def load_skill_definition(self, skill_id: str) -> SkillDefinition:
        """加载技能定义"""
        # 检查缓存
        if skill_id in self.skill_cache:
            return self.skill_cache[skill_id]

        # 加载技能定义
        skill_def = SkillDefinition.from_file(skill_id, self.skills_dir)

        # 缓存
        self.skill_cache[skill_id] = skill_def

        return skill_def

    def convert_parameters(
        self,
        user_params: Dict[str, Any],
        skill_def: SkillDefinition
    ) -> Dict[str, Any]:
        """
        转换用户参数为API参数格式

        Args:
            user_params: 用户输入参数（如 {"action": "open"}）
            skill_def: 技能定义

        Returns:
            API格式参数（完全符合SKILL.md规范）
        """
        # 使用技能定义中的参数模板作为基础
        if skill_def.param_template:
            api_params = skill_def.param_template.copy()
        else:
            # 如果没有模板，使用基本结构
            api_params = {
                "customInnerType": "nativeCommand",
                "object": skill_def.skill_id
            }

        # 根据用户参数更新模板中的值
        for key, value in user_params.items():
            if key == "action":
                # 映射action值
                if value in ["open", "打开", "开启", "启动"]:
                    api_params["action"] = "打开"
                elif value in ["close", "关闭", "停止"]:
                    api_params["action"] = "关闭"
                else:
                    api_params["action"] = str(value)

            elif key == "temperature":
                # 温度参数
                api_params["value"] = str(value)
                if "part" not in api_params:
                    api_params["part"] = "温度"

            elif key == "mode":
                # 模式参数
                if value == "auto" or value == "自动":
                    api_params["mode"] = "自动"
                    if "part" not in api_params:
                        api_params["part"] = "模式"
                else:
                    api_params["mode"] = str(value)

            elif key == "volume":
                # 音量参数
                if isinstance(value, (int, float)):
                    api_params["value"] = str(value)
                elif value in ["大", "高", "max", "up"]:
                    api_params["value"] = "high"
                elif value in ["小", "低", "min", "down"]:
                    api_params["value"] = "low"
                else:
                    api_params["value"] = "mid"

            elif key == "position":
                # 位置参数
                position_map = {
                    "front_left": "主驾", "driver": "主驾",
                    "front_right": "副驾", "passenger": "副驾",
                    "rear_left": "左后", "rear_right": "右后",
                    "all": "全车", "front": "前排", "rear": "后排"
                }
                if value in position_map:
                    api_params["zone"] = position_map[value]

            # 其他参数直接传递
            else:
                api_params[key] = value

        # 确保必要的字段存在
        if "customInnerType" not in api_params:
            api_params["customInnerType"] = "nativeCommand"

        if "object" not in api_params:
            api_params["object"] = skill_def.skill_id

        return api_params

    def _parse_example_params(self, example: str) -> Dict[str, Any]:
        """解析示例中的参数"""
        params = {}

        # 查找JSON格式的示例
        json_pattern = r'\{[^}]+\}'
        matches = re.findall(json_pattern, example)

        for match in matches:
            try:
                example_params = json.loads(match)
                params.update(example_params)
            except:
                pass

        return params

    def execute(
        self,
        skill_id: str,
        parameters: Dict[str, Any],
        user_id: str = "default"
    ) -> ExecutionResult:
        """
        执行技能

        Args:
            skill_id: 技能ID
            parameters: 参数字典
            user_id: 用户ID

        Returns:
            执行结果
        """
        start_time = time.perf_counter()

        try:
            # 1. 加载技能定义
            skill_def = self.load_skill_definition(skill_id)

            # 2. 转换参数格式
            api_params = self.convert_parameters(parameters, skill_def)

            # 3. 调用API
            response = self.api_client.call(skill_def.api, api_params)

            latency = (time.perf_counter() - start_time) * 1000

            # 4. 构建执行结果
            return ExecutionResult(
                skill_id=skill_id,
                execution_id=response.get('data', {}).get('execution_id', ''),
                status=response['status'],
                message=response['message'],
                api_called=skill_def.api,
                api_params=api_params,
                response_data=response.get('data', {}),
                error=None,
                latency_ms=latency
            )

        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000

            return ExecutionResult(
                skill_id=skill_id,
                execution_id='',
                status='failed',
                message=f'技能执行失败: {str(e)}',
                api_called='',
                api_params={},
                response_data={},
                error=str(e),
                latency_ms=latency
            )

    def batch_execute(
        self,
        instructions: List[Dict[str, Any]],
        user_id: str = "default"
    ) -> List[ExecutionResult]:
        """
        批量执行技能

        Args:
            instructions: 指令列表
                [{"skill_id": "OpenAC", "parameters": {"action": "open"}}, ...]

        Returns:
            执行结果列表
        """
        results = []

        for instruction in instructions:
            result = self.execute(
                instruction['skill_id'],
                instruction.get('parameters', {}),
                user_id
            )
            results.append(result)

        return results


def test_skill_executor():
    """测试技能执行器"""
    print("=" * 70)
    print("技能执行器测试")
    print("=" * 70)

    skills_dir = Path("E:/ai/py/whisperModel/vc/skills")

    # 初始化执行器
    executor = SkillExecutor(skills_dir, use_mock_api=True)

    # 测试用例
    test_cases = [
        {
            "name": "打开空调",
            "skill_id": "OpenAirConditionerMode",
            "parameters": {"action": "open"}
        },
        {
            "name": "设置温度",
            "skill_id": "AdjustAirConditionerAbsoluteTemperature",
            "parameters": {"temperature": 24}
        },
        {
            "name": "调大音量",
            "skill_id": "AdjustSpeedCompensatedVolume",
            "parameters": {"volume": "high"}
        },
        {
            "name": "座椅加热",
            "skill_id": "SeatHeat",
            "parameters": {"action": "heat"}
        },
    ]

    print(f"\n测试用例数: {len(test_cases)}")

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"测试 {i}: {test_case['name']}")
        print(f"{'='*70}")

        result = executor.execute(
            test_case['skill_id'],
            test_case['parameters']
        )

        print(f"技能ID: {result.skill_id}")
        print(f"执行ID: {result.execution_id}")
        print(f"状态: {result.status}")
        print(f"消息: {result.message}")
        print(f"API: {result.api_called}")
        print(f"延迟: {result.latency_ms:.2f} ms")

        if result.error:
            print(f"错误: {result.error}")

    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)


if __name__ == "__main__":
    test_skill_executor()
