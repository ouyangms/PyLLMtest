---
name: NoMicrophoneKaraoke
description: Toggle karaoke without microphone (控制车辆无麦k歌功能)
---

## 功能说明
- 控制车辆无麦k歌功能

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
        "app": "无麦K歌",
        "customInnerType": "nativeCommand",
        "feature": "系统应用",
        "action": "打开",
        "object": "屏幕"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `app` | string | app | `无麦K歌` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `feature` | string | feature | `系统应用` |
| `action` | string | action | `打开` |
| `object` | string | object | `屏幕` |

## 调用示例

### 示例 1
**用户输入**: 人声音量调大

```json
{
    "api": "sys.car.crl",
    "param": {
        "app": "无麦K歌",
        "customInnerType": "nativeCommand",
        "feature": "系统应用",
        "action": "关闭",
        "object": "屏幕"
    }
}
```

### 示例 2
**用户输入**: 人声音量调小

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "人声音量",
        "object": "整车",
        "value": "-",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭无麦k歌

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "人声音量",
        "object": "整车",
        "value": "+",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开无麦k歌

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "混音音量",
        "object": "整车",
        "value": "-",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 混音音量调大

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "混音音量",
        "object": "整车",
        "value": "+",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
