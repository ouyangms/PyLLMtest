---
name: QueryTripMileage
description: Query trip duration (查一下/查询本次里程行驶时长)
---

## 功能说明
- 查一下/查询本次里程行驶时长
- 查一下/查询本次里程行驶距离
- 查一下查询本次里程平均车速

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
        "action": "查看",
        "function": "行驶时长"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `查看` |
| `function` | string | function | `行驶时长` |

## 调用示例

### 示例 1
**用户输入**: 查一下本次里程平均车速

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "行驶时长"
    }
}
```

### 示例 2
**用户输入**: 查一下本次里程行驶时长

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "行驶距离"
    }
}
```

### 示例 3
**用户输入**: 查一下本次里程行驶距离

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "行驶距离"
    }
}
```

### 示例 4
**用户输入**: 查询本次里程平均车速

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "查看",
        "function": "里程平均车速",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 查询本次里程行驶时长

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "查看",
        "function": "里程平均车速",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
