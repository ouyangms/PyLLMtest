---
name: AdjustTopAngle
description: Adjust overhead screen angle (控制车辆吸顶屏角度调节功能)
---

## 功能说明
- 控制车辆吸顶屏角度调节功能

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
        "part": "角度",
        "object": "屏幕",
        "customInnerType": "nativeCommand",
        "value": "+",
        "position": "后排",
        "part_raw": "角度",
        "object_raw": "屏"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `角度` |
| `object` | string | object | `屏幕` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `+` |
| `position` | string | position | `后排` |
| `part_raw` | string | part_raw | `角度` |
| `object_raw` | string | object_raw | `屏` |

## 调用示例

### 示例 1
**用户输入**: 后排屏往外

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "屏幕",
        "customInnerType": "nativeCommand",
        "value": "外",
        "part": "方向",
        "position": "后排"
    }
}
```

### 示例 2
**用户输入**: 后排屏往里

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "屏幕",
        "part_raw": "角度",
        "object_raw": "屏",
        "customInnerType": "nativeCommand",
        "value": "-",
        "part": "角度",
        "position": "后排"
    }
}
```

### 示例 3
**用户输入**: 后排屏角度调到最大

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "屏幕",
        "action_concrete": "true",
        "part_raw": "角度",
        "object_raw": "屏",
        "customInnerType": "nativeCommand",
        "value": "min",
        "part": "角度",
        "position": "后排"
    }
}
```

### 示例 4
**用户输入**: 后排屏角度调到最小

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "屏幕",
        "customInnerType": "nativeCommand",
        "value": "内",
        "part": "方向",
        "position": "后排"
    }
}
```

### 示例 5
**用户输入**: 后排屏角度调大

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "屏幕",
        "part": "角度",
        "position": "后排",
        "customInnerType": "nativeCommand",
        "part_raw": "角度",
        "value": "max",
        "action_concrete": "true",
        "object_raw": "屏"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
