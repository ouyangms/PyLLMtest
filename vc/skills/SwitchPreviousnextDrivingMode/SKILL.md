---
name: SwitchPreviousnextDrivingMode
description: Switch to previous/next driving mode (上一个/下一个驾驶模式)
---

## 功能说明
- 上一个/下一个驾驶模式
- 性能/运动模式
- 性能模式
- 智能
- 智能电混/超级电混模式
- 纯电/舒适模式
- 经济/节能/增程/超级增程模式
- 行车模式
- 越野
- 雪地
- 雪地模式

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
        "action": "切换",
        "object": "整车",
        "part": "模式",
        "mode": "驾驶",
        "number": "-1",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `切换` |
| `object` | string | object | `整车` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `驾驶` |
| `number` | string | number | `-1` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭AutoTerrains模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "object": "整车",
        "part": "模式",
        "mode": "驾驶",
        "number": "+1",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭ECO模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "object": "整车",
        "part": "模式",
        "mode": "驾驶",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭Normal驾车模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "object": "整车",
        "part": "模式",
        "mode": "驾驶",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 关闭Snow驾驶模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "整车",
        "mode": "运动",
        "part": "模式",
        "action": "切换",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 关闭Sport模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "整车",
        "part": "模式",
        "object_raw": "驾驶",
        "mode": "节能",
        "part_raw": "模式",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
