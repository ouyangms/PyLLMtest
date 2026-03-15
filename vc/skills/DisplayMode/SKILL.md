---
name: DisplayMode
description: Set display theme to night/auto/custom/sunrise/sunset (将车辆显示主题设置为夜晚/自动/自定义/日出/日落)
---

## 功能说明
- 将车辆显示主题设置为夜晚/自动/自定义/日出/日落
- 显示模式切换为【浅色模式】
- 显示模式切换为【深色模式】
- 显示模式切换为【自动】

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
        "part": "模式",
        "mode": "自动",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true",
        "feature": "显示",
        "action": "切换"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `mode` | string | mode | `自动` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `屏幕` |
| `action_concrete` | string | action_concrete | `true` |
| `feature` | string | feature | `显示` |
| `action` | string | action | `切换` |

## 调用示例

### 示例 1
**用户输入**: 将车辆显示主题设置为夜晚

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "part_raw": "模式",
        "mode": "日落",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true",
        "feature": "显示"
    }
}
```

### 示例 2
**用户输入**: 将车辆显示主题设置为日出

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "part_raw": "模式",
        "mode": "日出",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true",
        "feature": "显示"
    }
}
```

### 示例 3
**用户输入**: 将车辆显示主题设置为日落

```json
{
    "api": "sys.car.crl",
    "param": {
        "mode": "日落",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "feature": "显示",
        "action_concrete": "true",
        "object": "屏幕"
    }
}
```

### 示例 4
**用户输入**: 将车辆显示主题设置为自动

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "屏幕",
        "mode": "自动",
        "feature": "显示",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "action_concrete": "true"
    }
}
```

### 示例 5
**用户输入**: 将车辆显示主题设置为自定义

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "屏幕",
        "mode": "自定义",
        "feature": "显示",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
