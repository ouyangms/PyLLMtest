---
name: OpenLaneKeepAssist
description: Open lane keep assist (控制车辆打开车道保持辅助功能)
---

## 功能说明
- 控制车辆打开车道保持辅助功能

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
        "subfunction": "车道保持辅助",
        "page": "页面",
        "function": "车道辅助",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `subfunction` | string | subfunction | `车道保持辅助` |
| `page` | string | page | `页面` |
| `function` | string | function | `车道辅助` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭车道保持辅助

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道保持辅助",
        "page": "设置",
        "function": "车道辅助",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```

### 示例 2
**用户输入**: 关闭车道保持辅助设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道保持辅助",
        "page": "页面",
        "function": "车道辅助",
        "customInnerType": "nativeCommand",
        "action": "关闭"
    }
}
```

### 示例 3
**用户输入**: 关闭车道保持辅助页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道保持辅助",
        "page": "设置",
        "function": "车道辅助",
        "customInnerType": "nativeCommand",
        "action": "关闭"
    }
}
```

### 示例 4
**用户输入**: 打开车道保持辅助

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道保持辅助",
        "function": "车道辅助",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```

### 示例 5
**用户输入**: 打开车道保持辅助设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道保持辅助",
        "function": "车道辅助",
        "customInnerType": "nativeCommand",
        "action": "关闭"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
