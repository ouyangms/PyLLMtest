---
name: SetAgileSteering
description: Close agile steering (关闭敏捷转向)
---

## 功能说明
- 关闭敏捷转向
- 关闭敏捷转向标准挡
- 打开敏捷转向
- 打开敏捷转向极致挡

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
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "敏捷转向"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `敏捷转向` |

## 调用示例

### 示例 1
**用户输入**: 关闭敏捷转向

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "敏捷转向",
        "part": "敏捷转向挡位",
        "value": "标准"
    }
}
```

### 示例 2
**用户输入**: 关闭敏捷转向标准挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "敏捷转向",
        "part": "敏捷转向挡位",
        "value": "极致"
    }
}
```

### 示例 3
**用户输入**: 打开敏捷转向

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "function": "敏捷转向",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开敏捷转向极致挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "function": "敏捷转向",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
