---
name: Charging
description: Toggle [交流/直流] charging port cover (打开/关闭[交流/直流]二合一充电口盖)
---

## 功能说明
- 打开/关闭【交流/直流】二合一充电口盖

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
        "feature": "交直流电",
        "customInnerType": "nativeCommand",
        "object_raw": "交流直流二合一充电口盖",
        "object": "充电盖"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `feature` | string | feature | `交直流电` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object_raw` | string | object_raw | `交流直流二合一充电口盖` |
| `object` | string | object | `充电盖` |

## 调用示例

### 示例 1
**用户输入**: 关闭交流直流二合一充电口盖

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "feature": "交直流电",
        "customInnerType": "nativeCommand",
        "object_raw": "交流直流二合一充电口盖",
        "object": "充电盖"
    }
}
```

### 示例 2
**用户输入**: 打开交流直流二合一充电口盖

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "feature": "交直流电",
        "customInnerType": "nativeCommand",
        "object_raw": "交流直流二合一充电口盖",
        "object": "充电盖"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
