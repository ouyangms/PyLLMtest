---
name: OpenMode
description: Toggle detailed/simple mode (控制车辆打开/关闭/切换为详细/简洁模式功能)
---

## 功能说明
- 控制车辆打开/关闭/切换为详细/简洁模式功能

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
        "part": "模式",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "mode": "详细"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `mode` | string | mode | `详细` |

## 调用示例

### 示例 1
**用户输入**: 关闭驾驶辅助语音播报精简模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "mode": "精简"
    }
}
```

### 示例 2
**用户输入**: 打开驾驶辅助语音播报详细模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "customInnerType": "nativeCommand",
        "action": "切换",
        "mode": "详细",
        "action_concrete": "true",
        "module": "语音",
        "function": "智慧巡航",
        "subfunction": "辅助驾驶播报"
    }
}
```

### 示例 3
**用户输入**: 驾驶辅助语音播报切换为精简模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "customInnerType": "nativeCommand",
        "action": "切换",
        "mode": "精简",
        "action_concrete": "true",
        "module": "语音",
        "function": "智慧巡航",
        "subfunction": "辅助驾驶播报"
    }
}
```

### 示例 4
**用户输入**: 驾驶辅助语音播报切换为详细模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "mode": "详细"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
