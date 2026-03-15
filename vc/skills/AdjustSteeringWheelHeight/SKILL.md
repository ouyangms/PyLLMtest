---
name: AdjustSteeringWheelHeight
description: Adjust steering wheel height (方向盘调高/调低+一点/百分之二十)
---

## 功能说明
- 方向盘调高/调低+一点/百分之二十
- 方向盘高度调到中间/百分之二十
- 方向盘高度调到最高/最低

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
        "value": "+",
        "part": "高度",
        "object": "方向盘"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `+` |
| `part` | string | part | `高度` |
| `object` | string | object | `方向盘` |

## 调用示例

### 示例 1
**用户输入**: 方向盘调低一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "+20/100",
        "part": "高度",
        "object": "方向盘"
    }
}
```

### 示例 2
**用户输入**: 方向盘调低百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "-",
        "part": "高度",
        "object": "方向盘"
    }
}
```

### 示例 3
**用户输入**: 方向盘调高一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "-20/100",
        "part": "高度",
        "object": "方向盘"
    }
}
```

### 示例 4
**用户输入**: 方向盘调高百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "mid",
        "part": "高度",
        "object": "方向盘"
    }
}
```

### 示例 5
**用户输入**: 方向盘高度调到中间

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "20/100",
        "part": "高度",
        "object": "方向盘"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
