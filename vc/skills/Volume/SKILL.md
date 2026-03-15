---
name: Volume
description: Toggle speed compensated volume (控制车辆音量随车速补偿功能)
---

## 功能说明
- 控制车辆音量随车速补偿功能

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
        "part": "音随车速档位",
        "feature": "音随车速",
        "action": "打开",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `音随车速档位` |
| `feature` | string | feature | `音随车速` |
| `action` | string | action | `打开` |
| `object` | string | object | `整车` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭音量随车速补偿

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音随车速档位",
        "feature": "音随车速",
        "action": "关闭",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭音量随车速补偿页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音随车速档位",
        "feature": "音随车速",
        "action": "打开",
        "object": "整车",
        "page": "设置",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 开启音量随车速补偿

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音随车速档位",
        "feature": "音随车速",
        "action": "关闭",
        "object": "整车",
        "page": "页面",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开音量随车速补偿设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "action_concrete": "true",
        "part": "音随车速档位",
        "feature": "音随车速",
        "customInnerType": "nativeCommand",
        "value": "low",
        "object": "整车"
    }
}
```

### 示例 5
**用户输入**: 音量随车速补偿切换为中

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "action_concrete": "true",
        "part": "音随车速档位",
        "feature": "音随车速",
        "customInnerType": "nativeCommand",
        "value": "mid",
        "object": "整车"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
