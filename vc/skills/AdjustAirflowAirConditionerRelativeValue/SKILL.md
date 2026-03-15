---
name: AdjustAirflowAirConditionerRelativeValue
description: Adjust [zone] air conditioner airflow relative value (控制车辆[zone]空调风量相对值调节功能)
---

## 功能说明
- 控制车辆【音区】空调风量相对值调节功能

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
        "part_raw": "风量",
        "part": "风力",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "+",
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
| `part_raw` | string | part_raw | `风量` |
| `part` | string | part | `风力` |
| `object_raw` | string | object_raw | `空调` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `+` |
| `object` | string | object | `空调` |

## 调用示例

### 示例 1
**用户输入**: 空调风量调低三挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "风量",
        "part": "风力",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "-",
        "object": "空调"
    }
}
```

### 示例 2
**用户输入**: 空调风量调大一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "风量",
        "part": "风力",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "+3",
        "object": "空调"
    }
}
```

### 示例 3
**用户输入**: 空调风量调小一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "风量",
        "part": "风力",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "value": "-3",
        "object": "空调"
    }
}
```

### 示例 4
**用户输入**: 空调风量调高三挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "风量",
        "part": "风力",
        "customInnerType": "nativeCommand",
        "value": "+20/100",
        "object": "空调"
    }
}
```

### 示例 5
**用户输入**: 风量调大百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "风量",
        "part": "风力",
        "customInnerType": "nativeCommand",
        "value": "-10/100",
        "object": "空调"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
