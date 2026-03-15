---
name: OpenSeatWelcomeMainAux
description: Close passenger seat welcome (关闭副驾座椅迎宾)
---

## 功能说明
- 关闭副驾座椅迎宾
- 打开主驾座椅迎宾

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
        "position": "主驾",
        "feature": "迎宾",
        "object": "座椅",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `position` | string | position | `主驾` |
| `feature` | string | feature | `迎宾` |
| `object` | string | object | `座椅` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭副驾座椅迎宾

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "position": "副驾",
        "feature": "迎宾",
        "object": "座椅",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开主驾座椅迎宾

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "function": "方便进出"
    }
}
```

### 示例 3
**用户输入**: 打开方便进出界面

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "position": "主驾",
        "feature": "迎宾",
        "object": "座椅",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
