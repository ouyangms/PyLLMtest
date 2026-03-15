---
name: Sunshade
description: Open/close sunshade (打开/关闭(遮阳帘|天窗遮阳帘|滑动天窗遮阳帘|全景式滑动天窗遮阳帘))
---

## 功能说明
- 打开/关闭(遮阳帘|天窗遮阳帘|滑动天窗遮阳帘|全景式滑动天窗遮阳帘)

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
        "object": "遮阳帘",
        "object_raw": "遮阳帘",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object` | string | object | `遮阳帘` |
| `object_raw` | string | object_raw | `遮阳帘` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭天窗遮阳帘

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "遮阳帘",
        "object": "遮阳帘",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭滑动天窗遮阳帘

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "遮阳帘",
        "object_raw": "遮阳帘",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭遮阳帘

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "天窗遮阳帘",
        "object": "遮阳帘",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 开启遮阳帘

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "遮阳帘",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 打开遮阳帘

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object": "遮阳帘",
        "object_raw": "遮阳帘",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
