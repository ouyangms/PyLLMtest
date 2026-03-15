---
name: OpenLeftRightChildLock
description: Open left/right child lock (控制车辆打开左/右儿童锁功能)
---

## 功能说明
- 控制车辆打开左/右儿童锁功能

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
        "object": "门锁",
        "position": "左",
        "feature": "儿童锁",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object` | string | object | `门锁` |
| `position` | string | position | `左` |
| `feature` | string | feature | `儿童锁` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 打开右边儿童锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object": "门锁",
        "position": "右",
        "feature": "儿童锁",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开左边儿童锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object": "门锁",
        "position": "左",
        "feature": "儿童锁",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
