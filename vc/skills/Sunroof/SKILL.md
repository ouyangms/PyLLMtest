---
name: Sunroof
description: Open | close sunroof (打开|关闭天窗)
---

## 功能说明
- 打开|关闭天窗

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
        "object_raw": "天窗",
        "customInnerType": "nativeCommand",
        "object": "天窗"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `天窗` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `天窗` |

## 调用示例

### 示例 1
**用户输入**: 关掉天窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "天窗",
        "object": "天窗",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭天窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "天窗",
        "object": "天窗",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 天窗关闭

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "天窗",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 开启天窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "天窗",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 我想晒晒太阳

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "天窗",
        "customInnerType": "nativeCommand",
        "object": "天窗"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
