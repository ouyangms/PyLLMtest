---
name: AdaptiveHeight
description: Toggle adaptive height (打开|关闭自适应高度)
---

## 功能说明
- 打开|关闭自适应高度

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
        "object": "HUD",
        "part": "模式",
        "mode": "自适应高度"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `HUD` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `自适应高度` |

## 调用示例

### 示例 1
**用户输入**: 关闭HUD自适应高度

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "HUD",
        "part": "模式",
        "mode": "自适应高度"
    }
}
```

### 示例 2
**用户输入**: 打开HUD自适应高度

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "HUD",
        "part": "模式",
        "mode": "自适应高度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
