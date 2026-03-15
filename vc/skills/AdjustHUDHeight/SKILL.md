---
name: AdjustHUDHeight
description: Adjust HUD height up/down (HUD往上/往下/向上/向下)
---

## 功能说明
- HUD往上/往下/向上/向下
- HUD高度调到一挡
- HUD高度调到最高/最低
- HUD高度调高/调低+一挡
- 保存/恢复抬头显示高度记忆
- 关闭HUD高度设置
- 打开HUD高度设置

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
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "1",
        "object": "HUD",
        "object_raw": "HUD",
        "part_raw": "高度"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `高度` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `1` |
| `object` | string | object | `HUD` |
| `object_raw` | string | object_raw | `HUD` |
| `part_raw` | string | part_raw | `高度` |

## 调用示例

### 示例 1
**用户输入**: HUD向上

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand",
        "part": "高度",
        "object": "HUD"
    }
}
```

### 示例 2
**用户输入**: HUD向下

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "part_raw": "高度",
        "value": "+1",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: HUD往上

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "part_raw": "高度",
        "value": "-1",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: HUD往下

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "max",
        "object": "HUD",
        "object_raw": "HUD",
        "part_raw": "高度"
    }
}
```

### 示例 5
**用户输入**: HUD调到最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "max",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "object": "HUD",
        "part": "高度",
        "object_raw": "HUD"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
