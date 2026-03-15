---
name: SetRearRow
description: Toggle | rear screen adjustment/settings page (打开|关闭后排屏调节/设置页)
---

## 功能说明
- 打开|关闭后排屏调节/设置页

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
        "page": "页面",
        "object": "屏幕",
        "position": "后排",
        "object_raw": "屏",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `page` | string | page | `页面` |
| `object` | string | object | `屏幕` |
| `position` | string | position | `后排` |
| `object_raw` | string | object_raw | `屏` |
| `action` | string | action | `关闭` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭后排屏调节页

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "object": "屏幕",
        "position": "后排",
        "object_raw": "屏",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开后排屏设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "object": "屏幕",
        "position": "后排",
        "object_raw": "屏",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
