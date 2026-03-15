---
name: AdjustMode
description: Set maintenance mode (雨刮竖立，处于维修模式，便于维修雨刮，无方向默认前雨刮)
---

## 功能说明
- 雨刮竖立，处于维修模式，便于维修雨刮，无方向默认前雨刮

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
        "action": "打开",
        "object": "雨刷",
        "mode": "维修",
        "part": "模式"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `object` | string | object | `雨刷` |
| `mode` | string | mode | `维修` |
| `part` | string | part | `模式` |

## 调用示例

### 示例 1
**用户输入**: 关闭雨刷维修模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "雨刷",
        "mode": "维修",
        "part": "模式"
    }
}
```

### 示例 2
**用户输入**: 打开雨刷维修模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "雨刷",
        "mode": "维修",
        "part": "模式"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
