---
name: SetRemoteUnlockModeDriverOnlywholeVehicl
description: Set remote unlock mode to driver only/whole vehicle (遥控解锁模式设置为仅主驾/整车)
---

## 功能说明
- 遥控解锁模式设置为仅主驾/整车

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
        "feature": "解锁",
        "mode": "主驾驶侧",
        "part_raw": "模式",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "object": "车钥匙"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `解锁` |
| `mode` | string | mode | `主驾驶侧` |
| `part_raw` | string | part_raw | `模式` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `模式` |
| `object` | string | object | `车钥匙` |

## 调用示例

### 示例 1
**用户输入**: 遥控解锁模式设置为仅主驾

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "解锁",
        "mode": "全车门",
        "part_raw": "模式",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "object": "车钥匙"
    }
}
```

### 示例 2
**用户输入**: 遥控解锁模式设置为整车

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "解锁",
        "mode": "主驾驶侧",
        "part_raw": "模式",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "object": "车钥匙"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
