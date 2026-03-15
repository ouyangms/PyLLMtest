---
name: AdjustEntertainmentAngle
description: Adjust second row entertainment screen angle (二排娱乐屏角度调大|二排娱乐屏往外|二排娱乐屏角度调小|二排娱乐屏往里|二排娱乐屏角度调到最大|二排娱乐屏角度调到最小)
---

## 功能说明
- 二排娱乐屏角度调大|二排娱乐屏往外|二排娱乐屏角度调小|二排娱乐屏往里|二排娱乐屏角度调到最大|二排娱乐屏角度调到最小

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
        "object": "娱乐屏",
        "customInnerType": "nativeCommand",
        "value": "+",
        "position": "第二排"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `角度` |
| `object` | string | object | `娱乐屏` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `+` |
| `position` | string | position | `第二排` |

## 调用示例

### 示例 1
**用户输入**: 二排娱乐屏大百分之三十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "object": "娱乐屏",
        "customInnerType": "nativeCommand",
        "value": "-",
        "position": "第二排"
    }
}
```

### 示例 2
**用户输入**: 二排娱乐屏开到最大

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "object": "娱乐屏",
        "customInnerType": "nativeCommand",
        "value": "+30/100",
        "position": "第二排"
    }
}
```

### 示例 3
**用户输入**: 二排娱乐屏开到最小

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "object": "娱乐屏",
        "customInnerType": "nativeCommand",
        "value": "50/100",
        "position": "第二排",
        "object_raw": "娱乐屏",
        "action_concrete": "true"
    }
}
```

### 示例 4
**用户输入**: 二排娱乐屏开大一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "object": "娱乐屏",
        "customInnerType": "nativeCommand",
        "value": "max",
        "position": "第二排",
        "action_concrete": "true"
    }
}
```

### 示例 5
**用户输入**: 二排娱乐屏开小一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "object": "娱乐屏",
        "customInnerType": "nativeCommand",
        "value": "min",
        "position": "第二排",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
