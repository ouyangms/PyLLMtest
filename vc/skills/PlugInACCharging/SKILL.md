---
name: PlugInACCharging
description: Set charging to 90% (充电设置到90%)
---

## 功能说明
- 充电设置到90%
- 关闭充电外部灯效
- 打开充电外部灯效

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
        "value": "90/100",
        "part_raw": "充电",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "充电限值",
        "object": "整车"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `value` | string | value | `90/100` |
| `part_raw` | string | part_raw | `充电` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `充电限值` |
| `object` | string | object | `整车` |

## 调用示例

### 示例 1
**用户输入**: 充电设置到90%

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "function": "充电外部灯效"
    }
}
```

### 示例 2
**用户输入**: 关闭充电外部灯效

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "function": "充电外部灯效"
    }
}
```

### 示例 3
**用户输入**: 打开充电外部灯效

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "90/100",
        "part_raw": "充电",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "充电限值",
        "object": "整车"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
