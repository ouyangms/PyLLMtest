---
name: PromptSound
description: Close safety alarm sound (关闭安全警报音)
---

## 功能说明
- 关闭安全警报音
- 切换安全警报提示音
- 打开安全警报音
- 调节安全警报提示音为中
- 调节安全警报提示音为快
- 调节安全警报提示音为慢

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
        "feature": "安全报警音",
        "action": "打开",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `安全报警音` |
| `action` | string | action | `打开` |
| `object` | string | object | `整车` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭安全警报音

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "安全报警音",
        "action": "关闭",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 切换安全警报提示音

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "安全报警音",
        "action": "切换",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 打开安全警报音

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "安全报警音",
        "object": "整车",
        "customInnerType": "nativeCommand",
        "part": "音量",
        "value": "low"
    }
}
```

### 示例 4
**用户输入**: 调节安全警报提示音为中

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "安全报警音",
        "object": "整车",
        "customInnerType": "nativeCommand",
        "part": "音量",
        "value": "high"
    }
}
```

### 示例 5
**用户输入**: 调节安全警报提示音为快

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "安全报警音",
        "object": "整车",
        "customInnerType": "nativeCommand",
        "part": "音量",
        "value": "mid",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
