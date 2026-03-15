---
name: ControlVehicleLocatingMode
description: Set vehicle locating mode to flash/horn+flash (寻车模式设置为闪灯/鸣笛+闪灯)
---

## 功能说明
- 寻车模式设置为闪灯/鸣笛+闪灯

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
        "action_concrete": "true",
        "object": "车灯",
        "value": "闪灯",
        "part_raw": "寻车",
        "part": "寻车",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action_concrete` | string | action_concrete | `true` |
| `object` | string | object | `车灯` |
| `value` | string | value | `闪灯` |
| `part_raw` | string | part_raw | `寻车` |
| `part` | string | part | `寻车` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 寻车模式设置为闪灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "车灯",
        "value": "鸣笛",
        "part_raw": "寻车",
        "part": "寻车",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 寻车模式设置为鸣笛

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "车灯",
        "value": "鸣笛闪灯",
        "part_raw": "寻车",
        "part": "寻车",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 寻车模式设置为鸣笛闪灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "车灯",
        "value": "闪灯",
        "part_raw": "寻车",
        "part": "寻车",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
