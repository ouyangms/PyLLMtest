---
name: NavigationMode
description: Set navigation mix mode to direct mix (将导航混音模式设置为直接混音)
---

## 功能说明
- 将导航混音模式设置为直接混音
- 将导航混音模式设置为自动混音

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
        "module": "导航",
        "action_concrete": "true",
        "value": "直接混音",
        "part": "混音方式",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `module` | string | module | `导航` |
| `action_concrete` | string | action_concrete | `true` |
| `value` | string | value | `直接混音` |
| `part` | string | part | `混音方式` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 将导航混音模式设置为直接混音

```json
{
    "api": "sys.car.crl",
    "param": {
        "module": "导航",
        "action_concrete": "true",
        "value": "自动混音",
        "part": "混音方式",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 将导航混音模式设置为自动混音

```json
{
    "api": "sys.car.crl",
    "param": {
        "module": "导航",
        "part": "混音方式",
        "customInnerType": "nativeCommand",
        "value": "直接混音",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
