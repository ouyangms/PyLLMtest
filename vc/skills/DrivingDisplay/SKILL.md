---
name: DrivingDisplay
description: Next boarding (下次上车)
---

## 功能说明
- 下次上车
- 关闭行车图案
- 打开关闭辅助驾驶联动
- 打开行车图案
- 无切换
- 每周
- 每天

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
        "function": "行车图案",
        "action": "打开",
        "object": "科技带灯",
        "page": "开关"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `行车图案` |
| `action` | string | action | `打开` |
| `object` | string | object | `科技带灯` |
| `page` | string | page | `开关` |

## 调用示例

### 示例 1
**用户输入**: 不自动切换行车图案

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "行车图案",
        "action": "关闭",
        "object": "科技带灯",
        "page": "开关"
    }
}
```

### 示例 2
**用户输入**: 关闭行车图案

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "customInnerType": "nativeCommand",
        "function": "行车图案",
        "mode": "无切换",
        "part": "模式",
        "object": "科技带灯"
    }
}
```

### 示例 3
**用户输入**: 关闭辅助驾驶联动

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "customInnerType": "nativeCommand",
        "function": "行车图案",
        "mode": "下次上车",
        "part": "模式",
        "object": "科技带灯",
        "action_concrete": "true"
    }
}
```

### 示例 4
**用户输入**: 打开行车图案

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "customInnerType": "nativeCommand",
        "function": "行车图案",
        "mode": "每天",
        "part": "模式",
        "object": "科技带灯",
        "action_concrete": "true"
    }
}
```

### 示例 5
**用户输入**: 打开辅助驾驶联动

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "customInnerType": "nativeCommand",
        "function": "行车图案",
        "mode": "每周",
        "part": "模式",
        "object": "科技带灯"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
