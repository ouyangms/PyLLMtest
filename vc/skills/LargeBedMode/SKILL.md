---
name: LargeBedMode
description: Toggle [front row/rear row/whole vehicle] bed mode (打开/关闭+前排/后排/全车大床模式)
---

## 功能说明
- 打开/关闭+前排/后排/全车大床模式
- 打开/关闭大床模式

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
        "mode": "成床",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `mode` | string | mode | `成床` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭全车大床模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "成床",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭前排大床模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "成床",
        "action": "打开",
        "position": "前排",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭后排大床模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "成床",
        "action": "打开",
        "position": "后排",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开全车大床模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "成床",
        "action": "打开",
        "position": "all",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 打开前排大床模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "成床",
        "action": "关闭",
        "position": "前排",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
