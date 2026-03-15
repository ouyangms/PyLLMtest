---
name: OpenSyncAirConditionerTemperature
description: Open air conditioner temperature sync (控制车辆打开空调温度同步功能)
---

## 功能说明
- 控制车辆打开空调温度同步功能

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
        "feature": "同步",
        "customInnerType": "nativeCommand",
        "part_raw": "温度",
        "object": "空调",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `温度` |
| `object_raw` | string | object_raw | `空调` |
| `feature` | string | feature | `同步` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part_raw` | string | part_raw | `温度` |
| `object` | string | object | `空调` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 打开气候同步

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "同步",
        "part_raw": "温度",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "打开",
        "part": "温度"
    }
}
```

### 示例 2
**用户输入**: 打开温度同步

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "同步",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "object_raw": "空调",
        "action": "打开"
    }
}
```

### 示例 3
**用户输入**: 打开空调同步

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "同步",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "打开",
        "part": "温度"
    }
}
```

### 示例 4
**用户输入**: 打开空调温度同步

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "空调",
        "feature": "同步",
        "customInnerType": "nativeCommand",
        "part_raw": "温度",
        "object": "空调",
        "action": "打开"
    }
}
```

### 示例 5
**用户输入**: 把空调同步打开

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "温度",
        "object_raw": "空调",
        "feature": "同步",
        "customInnerType": "nativeCommand",
        "part_raw": "温度",
        "object": "空调",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
