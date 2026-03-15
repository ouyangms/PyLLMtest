---
name: HUDHUD
description: Toggle HUD (打开/关闭+HUD/抬头显示)
---

## 功能说明
- 打开/关闭+HUD/抬头显示

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
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object` | string | object | `HUD` |
| `object_raw` | string | object_raw | `HUD` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭HUD

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭抬头显示

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object": "HUD",
        "object_raw": "抬头显示",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 打开HUD

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "HUD",
        "object_raw": "抬头显示",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开抬头显示

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
