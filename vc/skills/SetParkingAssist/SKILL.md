---
name: SetParkingAssist
description: Continue parking (继续泊车)
---

## 功能说明
- 继续泊车

## 调用逻辑
1. **意图解析**：系统自动识别用户指令中的操作意图和参数
2. **参数提取**：从用户自然语言中提取相关参数
3. **工具调用**：调用车辆控制工具执行相应操作

## 参数规范
用户输入自然语言指令后，LLM 需要提取参数并输出以下格式：

```json
{
    "api": "com.remoteParking.start",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "继续泊车"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `继续泊车` |

## 调用示例

### 示例 1
**用户输入**: 打开自动泊车

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "系统应用",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action": "打开",
        "app": "自动泊车"
    }
}
```

### 示例 2
**用户输入**: 继续泊车

```json
{
    "api": "com.remoteParking.start",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "继续泊车"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
