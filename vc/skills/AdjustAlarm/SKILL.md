---
name: AdjustAlarm
description: Adjust speed limit alarm mode (控制车辆限速报警方式调整功能)
---

## 功能说明
- 控制车辆限速报警方式调整功能

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
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "function": "交通标志",
        "subfunction": "限速提醒",
        "action": "关闭"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action_concrete` | string | action_concrete | `true` |
| `function` | string | function | `交通标志` |
| `subfunction` | string | subfunction | `限速提醒` |
| `action` | string | action | `关闭` |

## 调用示例

### 示例 1
**用户输入**: 限速报警方式调整为图标闪烁

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "交通标志",
        "subfunction": "限速提醒",
        "value": "图标闪烁"
    }
}
```

### 示例 2
**用户输入**: 限速报警方式调整为图标闪烁声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "交通标志",
        "subfunction": "限速提醒",
        "value": "图标闪烁声音"
    }
}
```

### 示例 3
**用户输入**: 限速报警方式调整为无报警

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "function": "交通标志",
        "subfunction": "限速提醒",
        "action": "关闭"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
