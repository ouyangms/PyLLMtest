---
name: AlarmVolume
description: Set alarm volume to high/medium/low (高中低)
---

## 功能说明
- 高中低

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
        "object": "整车",
        "feature": "车辆报警音",
        "part": "音量",
        "value": "+",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object` | string | object | `整车` |
| `feature` | string | feature | `车辆报警音` |
| `part` | string | part | `音量` |
| `value` | string | value | `+` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 整车报警音量设为中

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "整车",
        "feature": "车辆报警音",
        "part": "音量",
        "value": "mid",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 整车报警音量设为低

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "整车",
        "feature": "车辆报警音",
        "part": "音量",
        "value": "high",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 整车报警音量设为高

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "整车",
        "feature": "车辆报警音",
        "part": "音量",
        "value": "low",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 调低整车报警音量

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "整车",
        "feature": "车辆报警音",
        "part": "音量",
        "value": "-",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 调整车辆报警音量为中

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "customInnerType": "nativeCommand",
        "value": "high",
        "object": "整车",
        "feature": "车辆报警音",
        "part_raw": "音量"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
