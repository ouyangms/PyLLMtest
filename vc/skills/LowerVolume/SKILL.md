---
name: LowerVolume
description: Toggle lower media volume on door open (打开/关闭开门降低媒体音量)
---

## 功能说明
- 打开/关闭开门降低媒体音量
- 打开/关闭开门降低媒体音量设置

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
        "function": "开门降低音量",
        "module": "多媒体",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `开门降低音量` |
| `module` | string | module | `多媒体` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭开门降低媒体音量

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "开门降低音量",
        "module": "多媒体",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭开门降低媒体音量设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "开门降低音量",
        "module": "多媒体",
        "action": "打开",
        "page": "设置",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 打开开门降低媒体音量

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "开门降低音量",
        "module": "多媒体",
        "action": "关闭",
        "page": "设置",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开开门降低媒体音量设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "开门降低音量",
        "module": "多媒体",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
