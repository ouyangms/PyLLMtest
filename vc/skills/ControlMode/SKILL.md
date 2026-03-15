---
name: ControlMode
description: Set door handle unlock mode to driver only/whole vehicle (门把手感应解锁模式设置为仅主驾/整车)
---

## 功能说明
- 门把手感应解锁模式设置为仅主驾/整车

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
        "feature": "感应解锁",
        "object_raw": "门把手",
        "action_concrete": "true",
        "mode": "全车门",
        "object": "车门把手",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "part_raw": "模式"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `感应解锁` |
| `object_raw` | string | object_raw | `门把手` |
| `action_concrete` | string | action_concrete | `true` |
| `mode` | string | mode | `全车门` |
| `object` | string | object | `车门把手` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `模式` |
| `part_raw` | string | part_raw | `模式` |

## 调用示例

### 示例 1
**用户输入**: 门把手感应解锁模式设置为仅主驾

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "感应解锁",
        "object_raw": "门把手",
        "action_concrete": "true",
        "mode": "主驾驶侧",
        "object": "车门把手",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "part_raw": "模式"
    }
}
```

### 示例 2
**用户输入**: 门把手感应解锁模式设置为整车

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "感应解锁",
        "object_raw": "门把手",
        "action_concrete": "true",
        "mode": "全车门",
        "object": "车门把手",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "part_raw": "模式"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
