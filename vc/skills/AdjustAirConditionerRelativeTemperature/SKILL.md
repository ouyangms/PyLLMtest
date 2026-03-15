---
name: AdjustAirConditionerRelativeTemperature
description: Adjust [zone] air conditioner temperature relative value (控制车辆[zone]空调温度相对值调节功能)
---

## 功能说明
- 控制车辆【音区】空调温度相对值调节功能

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
        "part": "温度",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "+",
        "part_raw": "温度",
        "object": "空调"
    }
}
```

### 特殊参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `zone` | string | 音区参数（主驾音区/副驾音区/全车/一排/二排/三排） | `主驾音区` |

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `温度` |
| `object_raw` | string | object_raw | `空调` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `+` |
| `part_raw` | string | part_raw | `温度` |
| `object` | string | object | `空调` |

## 调用示例

### 示例 1
**用户输入**: 副驾温度太高了

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "风力",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "-",
        "part_raw": "风量",
        "object": "空调"
    }
}
```

### 示例 2
**用户输入**: 温度调低1度

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "温度",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "+3",
        "part_raw": "温度",
        "object": "空调"
    }
}
```

### 示例 3
**用户输入**: 空调冻死了

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "温度",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "-3",
        "part_raw": "温度",
        "object": "空调"
    }
}
```

### 示例 4
**用户输入**: 空调温度调低三度

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+2",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "object_raw": "空调",
        "part": "温度"
    }
}
```

### 示例 5
**用户输入**: 空调温度调低百分之十

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-1",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "part_raw": "温度",
        "part": "温度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
