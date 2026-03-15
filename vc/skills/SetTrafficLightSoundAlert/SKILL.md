---
name: SetTrafficLightSoundAlert
description: Toggle traffic light sound alert (控制车辆交通灯声音提醒功能)
---

## 功能说明
- 控制车辆交通灯声音提醒功能

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
        "subfunction": "交通灯提示",
        "action": "打开",
        "part": "预警方式",
        "function": "交通标志",
        "value": "声音",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `subfunction` | string | subfunction | `交通灯提示` |
| `action` | string | action | `打开` |
| `part` | string | part | `预警方式` |
| `function` | string | function | `交通标志` |
| `value` | string | value | `声音` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭交通灯声音提醒

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "交通灯提示",
        "action": "关闭",
        "part": "预警方式",
        "function": "交通标志",
        "value": "声音",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开交通灯声音提醒

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "交通灯提示",
        "action": "打开",
        "part": "预警方式",
        "function": "交通标志",
        "value": "声音",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
