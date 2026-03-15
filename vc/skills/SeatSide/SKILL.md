---
name: SeatSide
description: Adjust seat side wing to strong/weak (座椅侧翼+调到强/弱)
---

## 功能说明
- 座椅侧翼+调到强/弱
- 座椅侧翼+（强度）+调高/调低一点
- 座椅侧翼打开/关闭

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
        "customInnerType": "nativeCommand",
        "object": "座椅侧翼"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `座椅侧翼` |

## 调用示例

### 示例 1
**用户输入**: 座椅侧翼关闭

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "座椅侧翼"
    }
}
```

### 示例 2
**用户输入**: 座椅侧翼强度调低一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "弹性",
        "customInnerType": "nativeCommand",
        "object": "座椅侧翼",
        "value": "high",
        "action_concrete": "true"
    }
}
```

### 示例 3
**用户输入**: 座椅侧翼强度调高一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "弹性",
        "customInnerType": "nativeCommand",
        "object": "座椅侧翼",
        "value": "low",
        "action_concrete": "true"
    }
}
```

### 示例 4
**用户输入**: 座椅侧翼打开

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "弹性",
        "object": "座椅侧翼",
        "value": "+",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 座椅侧翼调到弱

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "弹性",
        "object": "座椅侧翼",
        "value": "-",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
