---
name: WelcomeOuter
description: Close external welcome light (关闭车外迎宾灯)
---

## 功能说明
- 关闭车外迎宾灯
- 打开车外迎宾灯

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
        "object_raw": "灯",
        "feature": "迎宾",
        "customInnerType": "nativeCommand",
        "position": "车外",
        "object": "车灯"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `灯` |
| `feature` | string | feature | `迎宾` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `position` | string | position | `车外` |
| `object` | string | object | `车灯` |

## 调用示例

### 示例 1
**用户输入**: 关闭车外迎宾灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "灯",
        "feature": "迎宾",
        "customInnerType": "nativeCommand",
        "position": "车外",
        "object": "车灯"
    }
}
```

### 示例 2
**用户输入**: 打开车外迎宾灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "灯",
        "feature": "迎宾",
        "customInnerType": "nativeCommand",
        "position": "车外",
        "object": "车灯"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
