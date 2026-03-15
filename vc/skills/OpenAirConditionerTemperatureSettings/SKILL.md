---
name: OpenAirConditionerTemperatureSettings
description: Open air conditioner temperature settings (控制车辆打开空调温度设置功能)
---

## 功能说明
- 控制车辆打开空调温度设置功能

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
        "page": "设置",
        "part": "温度",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "part_raw": "温度",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `page` | string | page | `设置` |
| `part` | string | part | `温度` |
| `object_raw` | string | object_raw | `空调` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `空调` |
| `part_raw` | string | part_raw | `温度` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 打开空调温度设置页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "part": "温度",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "part_raw": "温度",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
