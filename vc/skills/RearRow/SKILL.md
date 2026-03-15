---
name: RearRow
description: Toggle rear screen collision reminder (打开/关闭后排屏防碰撞提醒功能)
---

## 功能说明
- 打开/关闭后排屏防碰撞提醒功能

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
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "二排屏防碰撞提醒",
        "object": "娱乐屏"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `二排屏防碰撞提醒` |
| `object` | string | object | `娱乐屏` |

## 调用示例

### 示例 1
**用户输入**: 关闭后排屏防碰撞提醒功能

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "二排屏防碰撞提醒",
        "object": "娱乐屏"
    }
}
```

### 示例 2
**用户输入**: 打开后排屏防碰撞提醒功能

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "二排屏防碰撞提醒",
        "object": "娱乐屏"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
