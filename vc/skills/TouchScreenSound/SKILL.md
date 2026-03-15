---
name: TouchScreenSound
description: Close touch screen sound (关闭触摸屏声音)
---

## 功能说明
- 关闭触摸屏声音
- 打开触摸屏声音
- 设置触摸屏声音为经典

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
        "feature": "触屏音",
        "action": "打开",
        "object": "屏幕",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `触屏音` |
| `action` | string | action | `打开` |
| `object` | string | object | `屏幕` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭触摸屏声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "触屏音",
        "action": "关闭",
        "object": "屏幕",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开触摸屏声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音效",
        "sound": "经典",
        "feature": "触屏音",
        "action_concrete": "true",
        "object": "屏幕",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 设置触摸屏声音为经典

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "触屏音",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
