---
name: MainMain
description: Set display theme to day (将车辆显示主题设置为白天)
---

## 功能说明
- 将车辆显示主题设置为白天
- 将车辆显示主题设置为黑夜

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
        "mode": "日出",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true",
        "feature": "显示"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `mode` | string | mode | `日出` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `屏幕` |
| `action_concrete` | string | action_concrete | `true` |
| `feature` | string | feature | `显示` |

## 调用示例

### 示例 1
**用户输入**: 夜晚模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "mode": "日出",
        "part_raw": "模式",
        "object": "屏幕",
        "part": "模式",
        "object_raw": "显示",
        "customInnerType": "nativeCommand",
        "action_concrete": "true"
    }
}
```

### 示例 2
**用户输入**: 将车辆显示主题设置为白天

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "日落",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true",
        "feature": "显示"
    }
}
```

### 示例 3
**用户输入**: 将车辆显示主题设置为黑夜

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "模式",
        "object": "屏幕",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "mode": "日落"
    }
}
```

### 示例 4
**用户输入**: 车辆显示设置为白天模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "日出",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true",
        "feature": "显示"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
