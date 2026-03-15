---
name: ToggleStayPoweredWhenLeavingVehicle
description: Toggle stay powered on when leaving vehicle (打开/关闭离车不下电)
---

## 功能说明
- 打开/关闭离车不下电
- 离车下电开启x小时

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
        "function": "离车不下电",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `离车不下电` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭锁车不下电

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "离车不下电",
        "action": "关闭"
    }
}
```

### 示例 2
**用户输入**: 打开离车不下电

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "离车不下电",
        "action": "打开",
        "part": "时长",
        "value": "01:00:00"
    }
}
```

### 示例 3
**用户输入**: 离车不下电开启2小时

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "离车不下电",
        "action": "打开",
        "part": "时长",
        "value": "02:00:00"
    }
}
```

### 示例 4
**用户输入**: 离车不下电开启一小时

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "离车不下电",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
