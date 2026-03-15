---
name: Equalizer
description: Set equalizer to pop (均衡器音效调为流行)
---

## 功能说明
- 均衡器音效调为流行
- 将中音调到最大
- 将低/中/高音调大1
- 将低/中/高音调小一点
- 将高音调为5
- 打开均衡器设置

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
        "feature": "均衡器",
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "sound": "流行",
        "object": "整车",
        "part": "音效",
        "part_raw": "音效"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `均衡器` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action_concrete` | string | action_concrete | `true` |
| `sound` | string | sound | `流行` |
| `object` | string | object | `整车` |
| `part` | string | part | `音效` |
| `part_raw` | string | part_raw | `音效` |

## 调用示例

### 示例 1
**用户输入**: 均衡器音效调为流行

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "均衡器",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "page": "设置"
    }
}
```

### 示例 2
**用户输入**: 将中音调到最大

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "均衡器",
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "part_raw": "高音",
        "object": "整车",
        "part": "高音",
        "value": "5"
    }
}
```

### 示例 3
**用户输入**: 将中音调大1

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "均衡器",
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "part_raw": "中音",
        "object": "整车",
        "part": "中音",
        "value": "max"
    }
}
```

### 示例 4
**用户输入**: 将中音调小一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "均衡器",
        "customInnerType": "nativeCommand",
        "part_raw": "低音",
        "object": "整车",
        "part": "低音",
        "value": "+1"
    }
}
```

### 示例 5
**用户输入**: 将低音调大1

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "均衡器",
        "customInnerType": "nativeCommand",
        "part_raw": "中音",
        "object": "整车",
        "part": "中音",
        "value": "+1"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
