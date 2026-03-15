---
name: SetModeWarning
description: Set lane departure warning mode (控制车辆设置车道偏离预警模式功能)
---

## 功能说明
- 控制车辆设置车道偏离预警模式功能

## 调用逻辑
1. **意图解析**：系统自动识别用户指令中的操作意图和参数
2. **参数提取**：从用户自然语言中提取相关参数
3. **工具调用**：调用车辆控制工具执行相应操作

## 参数规范
用户输入自然语言指令后，LLM 需要提取参数并输出以下格式：

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道偏离",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "车道辅助",
        "value": "震动",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `subfunction` | string | subfunction | `车道偏离` |
| `action_concrete` | string | action_concrete | `true` |
| `part` | string | part | `预警方式` |
| `function` | string | function | `车道辅助` |
| `value` | string | value | `震动` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 车道偏离预警模式设置为声音模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道偏离",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "车道辅助",
        "value": "声音",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 车道偏离预警模式设置为震动模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道偏离",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "车道辅助",
        "value": "震动",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
