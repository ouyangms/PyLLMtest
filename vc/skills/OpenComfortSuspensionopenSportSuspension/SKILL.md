---
name: OpenComfortSuspensionopenSportSuspension
description: Open comfort suspension/open sport suspension (打开舒适悬架/打开运动悬架)
---

## 功能说明
- 打开舒适悬架/打开运动悬架

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
        "object_raw": "悬架",
        "customInnerType": "nativeCommand",
        "object": "悬架",
        "part": "模式",
        "mode": "舒适",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object_raw` | string | object_raw | `悬架` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `悬架` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `舒适` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭舒适悬架

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "customInnerType": "nativeCommand",
        "object": "悬架",
        "part": "模式",
        "mode": "舒适",
        "action": "关闭"
    }
}
```

### 示例 2
**用户输入**: 关闭运动悬架

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "customInnerType": "nativeCommand",
        "object": "悬架",
        "part": "模式",
        "mode": "运动",
        "action": "打开"
    }
}
```

### 示例 3
**用户输入**: 打开舒适悬架

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "customInnerType": "nativeCommand",
        "object": "悬架",
        "part": "模式",
        "mode": "运动",
        "action": "关闭"
    }
}
```

### 示例 4
**用户输入**: 打开运动悬架

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "customInnerType": "nativeCommand",
        "object": "悬架",
        "part": "模式",
        "mode": "舒适",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
