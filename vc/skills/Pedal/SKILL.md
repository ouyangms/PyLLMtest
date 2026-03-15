---
name: Pedal
description: Set brake pedal to comfortable/sport (制动踏板设为舒适/运动)
---

## 功能说明
- 制动踏板设为舒适/运动

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
        "object_raw": "制动踏板",
        "mode": "舒适",
        "customInnerType": "nativeCommand",
        "object": "制动踏板",
        "action": "切换",
        "action_concrete": "true"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `object_raw` | string | object_raw | `制动踏板` |
| `mode` | string | mode | `舒适` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `制动踏板` |
| `action` | string | action | `切换` |
| `action_concrete` | string | action_concrete | `true` |

## 调用示例

### 示例 1
**用户输入**: 制动踏板切换为舒适

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "object_raw": "制动踏板",
        "mode": "运动",
        "customInnerType": "nativeCommand",
        "object": "制动踏板",
        "action": "切换",
        "action_concrete": "true"
    }
}
```

### 示例 2
**用户输入**: 制动踏板切换为运动

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "object_raw": "制动踏板",
        "mode": "舒适",
        "customInnerType": "nativeCommand",
        "object": "制动踏板",
        "action": "切换",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
