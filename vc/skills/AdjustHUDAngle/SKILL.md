---
name: AdjustHUDAngle
description: Adjust HUD angle to maximum/minimum (HUD角度调到最大/最小)
---

## 功能说明
- HUD角度调到最大/最小
- HUD角度调到百分之二十
- HUD角度调大/调小+一点/百分之二十
- 保存/恢复抬头显示角度记忆
- 关闭HUD角度设置
- 打开HUD角度设置

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
        "part": "角度",
        "part_raw": "角度",
        "value": "+",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `角度` |
| `part_raw` | string | part_raw | `角度` |
| `value` | string | value | `+` |
| `object` | string | object | `HUD` |
| `object_raw` | string | object_raw | `HUD` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: HUD角度调到最大

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "part_raw": "角度",
        "value": "-",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: HUD角度调到最小

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "part_raw": "角度",
        "value": "+20/100",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: HUD角度调到百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "part_raw": "角度",
        "value": "-20/100",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: HUD角度调大一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "20/100",
        "object": "HUD",
        "object_raw": "HUD",
        "part_raw": "角度"
    }
}
```

### 示例 5
**用户输入**: HUD角度调大百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "max",
        "object": "HUD",
        "object_raw": "HUD",
        "part_raw": "角度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
