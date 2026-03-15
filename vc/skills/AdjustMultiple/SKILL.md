---
name: AdjustMultiple
description: Adjust sunroof to 50% ([前/后/全部]天幕开到50%)
---

## 功能说明
- 【前/后/全部】天幕开到50%
- 【前/后/全部】天幕开大30%
- 【前/后/全部】遮阳帘开到50%
- 【前/后/全部】遮阳帘开大30%
- 对车窗开度进行特定值参数调节

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
        "value": "50/100",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "前排",
        "action_concrete": "true"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `50/100` |
| `part` | string | part | `幅度` |
| `action` | string | action | `打开` |
| `object` | string | object | `车窗` |
| `position` | string | position | `前排` |
| `action_concrete` | string | action_concrete | `true` |

## 调用示例

### 示例 1
**用户输入**: 全车车窗开到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "50/100",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "左",
        "action_concrete": "true"
    }
}
```

### 示例 2
**用户输入**: 全部天幕开到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "50/100",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "all",
        "action_concrete": "true"
    }
}
```

### 示例 3
**用户输入**: 全部天幕开小30%

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "-30/100",
        "part": "幅度",
        "action": "打开",
        "object": "遮阳帘",
        "position": "前"
    }
}
```

### 示例 4
**用户输入**: 全部遮阳帘开到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "-30/100",
        "part": "幅度",
        "action": "打开",
        "object": "遮阳帘",
        "position": "后"
    }
}
```

### 示例 5
**用户输入**: 全部遮阳帘开小30%

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "+30/100",
        "part": "幅度",
        "action": "打开",
        "object": "遮阳帘",
        "position": "all"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
