---
name: SetEnergyConsumptionCurve
description: Switch energy consumption curve to year (能耗曲线切换为年)
---

## 功能说明
- 能耗曲线切换为年
- 能耗曲线切换为日
- 能耗曲线切换为月
- 能耗曲线切换为油耗
- 能耗曲线切换为电耗
- 能耗曲线切换为近100km
- 能耗曲线切换为近50km

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
        "function": "能耗曲线",
        "action": "切换",
        "value": "电耗"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `能耗曲线` |
| `action` | string | action | `切换` |
| `value` | string | value | `电耗` |

## 调用示例

### 示例 1
**用户输入**: 能耗曲线切换为年

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "能耗曲线",
        "action": "切换",
        "value": "油耗"
    }
}
```

### 示例 2
**用户输入**: 能耗曲线切换为日

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "能耗曲线",
        "action": "切换",
        "value": "近50"
    }
}
```

### 示例 3
**用户输入**: 能耗曲线切换为月

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "能耗曲线",
        "action": "切换",
        "value": "近100"
    }
}
```

### 示例 4
**用户输入**: 能耗曲线切换为油耗

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "能耗曲线",
        "action": "切换",
        "value": "日"
    }
}
```

### 示例 5
**用户输入**: 能耗曲线切换为电耗

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "能耗曲线",
        "action": "切换",
        "value": "月"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
