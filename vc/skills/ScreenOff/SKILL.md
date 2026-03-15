---
name: ScreenOff
description: Close second row screen (关闭二排屏幕)
---

## 功能说明
- 关闭二排屏幕
- 将二排屏幕熄屏

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
        "action": "关闭",
        "object": "屏幕",
        "object_raw": "屏幕",
        "customInnerType": "nativeCommand",
        "position": "第二排"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `object` | string | object | `屏幕` |
| `object_raw` | string | object_raw | `屏幕` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `position` | string | position | `第二排` |

## 调用示例

### 示例 1
**用户输入**: 关闭二排屏幕

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "屏幕",
        "object_raw": "屏幕",
        "customInnerType": "nativeCommand",
        "position": "第二排"
    }
}
```

### 示例 2
**用户输入**: 将二排屏幕熄屏

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "屏幕",
        "object_raw": "屏幕",
        "customInnerType": "nativeCommand",
        "position": "第二排"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
