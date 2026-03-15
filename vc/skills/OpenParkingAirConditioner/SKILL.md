---
name: OpenParkingAirConditioner
description: Toggle parking air conditioner (控制车辆打开关闭把驻车空调功能)
---

## 功能说明
- 控制车辆打开关闭把驻车空调功能

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
        "function": "驻车",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "object_raw": "空调"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `驻车` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `空调` |
| `object_raw` | string | object_raw | `空调` |

## 调用示例

### 示例 1
**用户输入**: 关闭驻车空调

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "空调",
        "function": "驻车",
        "customInnerType": "nativeCommand",
        "mode": "通风",
        "part_raw": "模式",
        "part": "模式"
    }
}
```

### 示例 2
**用户输入**: 帮我把驻车空调关掉

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "空调",
        "action_concrete": "true",
        "part_raw": "模式",
        "function": "驻车",
        "customInnerType": "nativeCommand",
        "mode": "智能",
        "object_raw": "空调",
        "part": "模式"
    }
}
```

### 示例 3
**用户输入**: 帮我把驻车空调开启

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "驻车",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "object_raw": "空调"
    }
}
```

### 示例 4
**用户输入**: 打开驻车空调

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "驻车",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "object_raw": "空调"
    }
}
```

### 示例 5
**用户输入**: 把驻车空调切换到智能模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "驻车",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "object_raw": "空调"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
