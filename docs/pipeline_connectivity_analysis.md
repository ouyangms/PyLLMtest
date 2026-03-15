# 车控技能路由系统 - 流程联通性分析报告

## 执行摘要

对当前系统的完整流程进行联通性检查，发现**前4个环节已联通**，但**缺少关键的技能执行环节**。

---

## 完整流程设计

```
用户输入 ("打开空调")
    ↓
┌─────────────────────────────────────────────────────┐
│ 第1步: 路由分类                                     │
│ - 模型: TextCNNLite                                │
│ - 输入: 用户文本                                    │
│ - 输出: 类别 (climate_control)                       │
│ - 准确率: 100%                                       │
│ - 延迟: ~1ms                                         │
└─────────────────────────────────────────────────────┘
    ↓ category = "climate_control"
┌─────────────────────────────────────────────────────┐
│ 第2步: 技能检索                                     │
│ - 检索器: HybridRetriever (混合检索)                 │
│ - 输入: 类别 + 用户查询                             │
│ - 输出: Top-3 技能候选                               │
│ - 准确率: 76.67%                                     │
│ - 延迟: ~2.5ms                                       │
│ - 示例输出:                                         │
│   [                                                 │
│     {                                             │
│       "skill_id": "OpenAC",                       │
│       "name": "打开空调",                          │
│       "similarity": 0.90                           │
│     },                                            │
│     {                                             │
│       "skill_id": "SetTemperature",               │
│       "name": "设置空调温度",                      │
│       "similarity": 0.70                           │
│     }                                             │
│   ]                                             │
└─────────────────────────────────────────────────────┘
    ↓ candidates
┌─────────────────────────────────────────────────────┐
│ 第3步: LLM意图解析                                 │
│ - 解析器: LLMParser (规则引擎)                      │
│ - 输入: 用户查询 + 技能候选                          │
│ - 输出: 技能ID + 参数                                │
│ - 当前: 规则引擎，未集成真实LLM                      │
│ - 延迟: ~0.5ms                                      │
│ - 示例输出:                                        │
│   {                                             │
│     "skill_id": "OpenAC",                         │
│     "parameters": {"action": "open"},              │
│     "confidence": 0.90,                            │
│     "reasoning": "基于关键词匹配"                   │
│   }                                             │
└─────────────────────────────────────────────────────┘
    ↓ skill_id + parameters
┌─────────────────────────────────────────────────────┐
│ 第4步: 技能执行 (❌ 缺失)                          │
│ - 执行器: SkillExecutor (未实现)                   │
│ - 输入: 技能ID + 参数                              │
│ - 输出: API调用结果                                │
│ - 需要实现:                                        │
│   1. 根据skill_id找到技能定义                      │
│   2. 将参数转换为API格式                          │
│   3. 调用车辆控制API (sys.car.crl)                 │
│   4. 返回执行结果                                  │
└─────────────────────────────────────────────────────┘
    ↓ execution_result
┌─────────────────────────────────────────────────────┐
│ 第5步: 输出结果 (✅ 部分实现)                      │
│ - 当前: 返回技能信息                               │
│ - 需要: 返回执行结果 + 状态反馈                    │
└─────────────────────────────────────────────────────┘
```

---

## 当前状态分析

### ✅ 已实现的环节

#### 1. 路由分类 (100%完成)

**文件**: `src/router/textcnn_model.py`, `src/router/contextual_dialog.py`

**功能**:
- TextCNNLite模型（187K参数）
- 字符级输入，13个分类输出
- 准确率: 100% (清洗后数据)
- 延迟: ~1ms

**接口**:
```python
router = ContextualDialogRouter(model_path, device)
result = router.process_input(user_text, user_id)
# 输出: {'category': 'climate_control', 'confidence': 0.95}
```

#### 2. 技能检索 (100%完成)

**文件**: `src/hybrid/hybrid_retriever.py`

**功能**:
- 混合检索（关键词0.3 + 向量0.7）
- bge-small-zh-v1.5 embedding
- GPU加速支持
- 检索准确率: 76.67%
- 延迟: ~2.5ms

**接口**:
```python
retriever = HybridRetriever(skills_dir, use_embedding=True)
candidates = retriever.retrieve(query, category, top_k=3)
# 输出: [{'skill_id': 'OpenAC', 'similarity': 0.90}, ...]
```

#### 3. LLM意图解析 (80%完成)

**文件**: `src/hybrid/llm_parser.py`

**当前状态**: 使用规则引擎

**功能**:
- 参数提取（数字、位置、开关状态）
- 置信度计算
- 相似度评分

**缺失**:
- ❌ 真实LLM集成（Gemma-3-1B-IT）
- ❌ 复杂意图理解
- ❌ 多参数处理

**接口**:
```python
parser = LLMParser(use_local_llm=False)
result = parser.parse_intent(user_input, candidates, context)
# 输出: ParsedResult(skill_id, parameters, confidence, reasoning)
```

#### 4. 结果输出 (60%完成)

**文件**: `src/hybrid/inference_engine_v2.py`

**当前状态**: 返回技能信息，未执行

**功能**:
- 返回InferenceResult对象
- 包含skill_id, parameters, confidence等
- 延迟统计

**缺失**:
- ❌ 实际API调用
- ❌ 执行结果反馈
- ❌ 状态确认

### ❌ 缺失的环节

#### 1. 技能执行器 (0%完成)

**需要实现**:
```python
class SkillExecutor:
    """技能执行器 - 调用车辆控制API"""

    def execute(self, skill_id: str, parameters: Dict) -> ExecutionResult:
        """
        执行技能

        Args:
            skill_id: 技能ID (如 "OpenAC")
            parameters: 参数 (如 {"action": "open"})

        Returns:
            ExecutionResult(execution_id, status, message, data)
        """
        # 1. 加载技能定义
        skill_def = self._load_skill_definition(skill_id)

        # 2. 转换参数格式
        api_params = self._convert_parameters(skill_def, parameters)

        # 3. 调用API
        response = self._call_vehicle_api(api_params)

        # 4. 返回结果
        return ExecutionResult(...)
```

**需要支持的功能**:
- 根据skill_id加载SKILL.md文件
- 解析参数规范（params_schema）
- 将参数转换为API格式
- 调用sys.car.crl等车辆控制API
- 处理API响应
- 错误处理和重试

#### 2. LLM集成 (20%完成)

**需要实现**:
- 集成Gemma-3-1B-IT或其他本地LLM
- 实现真正的意图理解
- 复杂参数提取
- 上下文理解

---

## 技能定义格式分析

基于 `AdjustAirConditionerAbsoluteTemperature/SKILL.md`:

### 参数格式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "part": "温度",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "20",
        "part_raw": "温度",
        "object": "空调"
    }
}
```

### 关键字段

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `api` | API名称 | `sys.car.crl` |
| `part` | 控制的部分 | `温度` |
| `object` | 控制的对象 | `空调` |
| `value` | 参数值 | `20`, `mid`, `high` |
| `action_concrete` | 具体动作 | `true`/`false` |
| `customInnerType` | 自定义类型 | `nativeCommand` |

---

## 需要实现的组件

### 1. 技能执行器

**文件**: `src/hybrid/skill_executor.py`

**核心功能**:
```python
class SkillExecutor:
    def __init__(self, skills_dir: Path, api_client):
        self.skills_dir = skills_dir
        self.api_client = api_client  # API客户端

    def execute(self, skill_id: str, parameters: Dict) -> ExecutionResult:
        # 加载技能定义
        skill_def = self._load_skill(skill_id)

        # 构建API参数
        api_params = self._build_api_params(skill_def, parameters)

        # 调用API
        response = self.api_client.call(
            api=skill_def['api'],
            params=api_params
        )

        return ExecutionResult(
            skill_id=skill_id,
            status=response['status'],
            message=response['message'],
            data=response.get('data', {})
        )
```

### 2. API客户端

**文件**: `src/hybrid/vehicle_api_client.py`

**核心功能**:
```python
class VehicleAPIClient:
    """车辆控制API客户端"""

    def __init__(self, api_base: str, auth_token: str):
        self.api_base = api_base
        self.auth_token = auth_token

    def call(self, api: str, params: Dict) -> Dict:
        """
        调用车辆控制API

        示例:
        call("sys.car.crl", {"part": "温度", "value": "20"})
        """
        # 实现HTTP调用
        # 处理认证
        # 错误处理
        pass
```

---

## 优先级建议

### 高优先级（必须实现）

1. **技能执行器** - 核心缺失环节
   - 加载SKILL.md
   - 参数格式转换
   - API调用封装

2. **模拟API客户端** - 用于开发测试
   - 模拟车辆控制API
   - 返回模拟结果
   - 支持测试场景

### 中优先级（增强功能）

1. **真实LLM集成** - 提升智能化
   - 集成Gemma-3-1B-IT
   - 复杂意图理解
   - 多参数提取

2. **真实API客户端** - 生产环境
   - HTTP/HTTPS调用
   - 认证和授权
   - 错误处理和重试

### 低优先级（优化功能）

1. **执行历史记录**
2. **状态监控**
3. **批量执行**

---

## 当前可用流程

虽然缺少技能执行环节，但以下功能已完全可用：

### 可用于

✅ **技能推荐系统**
- 用户输入 → 技能推荐
- 展示技能信息
- 参数建议

✅ **意图识别系统**
- 用户意图分类
- 技能检索
- 参数提取

✅ **对话系统**
- 多轮对话
- 上下文理解
- 模糊输入处理

### 不可用于

❌ **实际车辆控制**
- 缺少API调用
- 缺少执行反馈

❌ **完整自动化**
- 无法闭环执行

---

## 实施建议

### 第一阶段：技能执行器（1-2天）

1. 创建 `src/hybrid/skill_executor.py`
2. 实现技能定义加载
3. 实现参数格式转换
4. 创建模拟API客户端
5. 集成到推理引擎V2

### 第二阶段：真实API集成（3-5天）

1. 创建 `src/hybrid/vehicle_api_client.py`
2. 实现真实API调用
3. 处理认证和错误
4. 集成执行结果反馈

### 第三阶段：LLM集成（1周）

1. 集成Gemma-3-1B-IT
2. 实现真正的意图理解
3. 优化参数提取
4. 上下文理解增强

---

## 总结

### 当前状态

**已联通**: 4/6个环节
- ✅ 用户输入 → 路由分类 → 技能检索 → LLM解析 → 输出结果
- ❌ 缺少技能执行环节

**核心问题**: 系统能识别和推荐技能，但**无法实际执行**

### 系统能力

**当前可用**:
- 智能技能推荐
- 意图识别和分类
- 参数提取和建议
- 多轮对话

**需要补充**:
- 技能执行器
- API调用
- 执行结果反馈

### 优先级

**立即实施**: 技能执行器 + 模拟API
**后续实施**: 真实API + LLM集成

---

**报告日期**: 2024年
**版本**: v1.0
**状态**: ⚠️ 流程部分联通，缺少执行环节
