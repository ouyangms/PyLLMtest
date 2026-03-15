---
name: Screensaver
description: Toggle | screensaver (settings) (打开|关闭屏保(设置))
---

## 功能说明
- 打开|关闭屏保(设置)

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
        "page": "设置",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object_raw": "屏",
        "object": "屏幕",
        "feature": "保护"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `page` | string | page | `设置` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `屏` |
| `object` | string | object | `屏幕` |
| `feature` | string | feature | `保护` |

## 调用示例

### 示例 1
**用户输入**: 关闭屏保

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "屏幕",
        "object_raw": "屏",
        "customInnerType": "nativeCommand",
        "feature": "保护"
    }
}
```

### 示例 2
**用户输入**: 打开屏保设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object_raw": "屏",
        "object": "屏幕",
        "feature": "保护"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
