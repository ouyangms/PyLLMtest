---
name: SteeringWheelTemperature
description: Open steering wheel temperature settings (打开方向盘温度设置)
---

## 功能说明
- 打开方向盘温度设置
- 方向盘温度调到一挡
- 方向盘温度调到最高/最低
- 方向盘温度调高/调低一挡

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
        "object_raw": "方向盘",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "1",
        "object": "方向盘",
        "feature": "加热",
        "part_raw": "温度"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `温度` |
| `object_raw` | string | object_raw | `方向盘` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `1` |
| `object` | string | object | `方向盘` |
| `feature` | string | feature | `加热` |
| `part_raw` | string | part_raw | `温度` |

## 调用示例

### 示例 1
**用户输入**: 打开方向盘温度设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "温度",
        "object": "方向盘",
        "customInnerType": "nativeCommand",
        "value": "+1",
        "feature": "加热",
        "object_raw": "方向盘",
        "part_raw": "温度"
    }
}
```

### 示例 2
**用户输入**: 方向盘温度调低一挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "温度",
        "object": "方向盘",
        "customInnerType": "nativeCommand",
        "value": "-1",
        "feature": "加热",
        "object_raw": "方向盘",
        "part_raw": "温度"
    }
}
```

### 示例 3
**用户输入**: 方向盘温度调到一挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "温度",
        "object_raw": "方向盘",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "max",
        "object": "方向盘",
        "feature": "加热",
        "part_raw": "温度"
    }
}
```

### 示例 4
**用户输入**: 方向盘温度调到最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "温度",
        "object_raw": "方向盘",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "min",
        "object": "方向盘",
        "feature": "加热",
        "part_raw": "温度"
    }
}
```

### 示例 5
**用户输入**: 方向盘温度调到最高

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "设置",
        "part": "温度",
        "object": "方向盘",
        "customInnerType": "nativeCommand",
        "object_raw": "方向盘",
        "part_raw": "温度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
