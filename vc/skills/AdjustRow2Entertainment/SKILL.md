---
name: AdjustRow2Entertainment
description: Adjust second row entertainment screen position to X% (二排娱乐屏前后调到X%)
---

## 功能说明
- 二排娱乐屏前后调到X%
- 二排娱乐屏向前/向后调一点
- 二排娱乐屏往前/往后+X%
- 二排娱乐屏调到最前|最后

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
        "part": "方向",
        "object_raw": "娱乐屏",
        "object": "娱乐屏",
        "position": "第二排",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "50/100"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `方向` |
| `object_raw` | string | object_raw | `娱乐屏` |
| `object` | string | object | `娱乐屏` |
| `position` | string | position | `第二排` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `50/100` |

## 调用示例

### 示例 1
**用户输入**: 二排娱乐屏位置设为到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "direction_range": "30/100",
        "object": "娱乐屏",
        "object_raw": "娱乐屏",
        "position": "第二排",
        "customInnerType": "nativeCommand",
        "value": "前"
    }
}
```

### 示例 2
**用户输入**: 二排娱乐屏向前调一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "direction_range": "30/100",
        "object": "娱乐屏",
        "object_raw": "娱乐屏",
        "position": "第二排",
        "customInnerType": "nativeCommand",
        "value": "后"
    }
}
```

### 示例 3
**用户输入**: 二排娱乐屏向前调节30%

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "前",
        "position": "第二排",
        "object": "娱乐屏",
        "part": "方向",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 二排娱乐屏向后调一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "后",
        "position": "第二排",
        "object": "娱乐屏",
        "part": "方向",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 二排娱乐屏向后调节30%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "object_raw": "娱乐屏",
        "direction_range": "max",
        "object": "娱乐屏",
        "value": "前",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "position": "第二排"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
