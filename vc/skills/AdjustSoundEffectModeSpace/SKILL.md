---
name: AdjustSoundEffectModeSpace
description: Adjust sound effect mode (1、当前在播放全景声/全车沉浸环统音效/2D环绕音效开启)
---

## 功能说明
- 1、当前在播放全景声/全车沉浸环统音效/2D环绕音效开启
- 1、当前在播放全景声/全车沉浸环统音效/2D环绕音效开启
- 1、当前在播放全景声/全车沉浸环统音效/2D环绕音效开启
- 1、当前在播放全景声/全车沉浸环统音效/2D环绕音效开启
- 默认全车

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
        "page": "设置",
        "object": "整车",
        "part": "空间音效",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `page` | string | page | `设置` |
| `object` | string | object | `整车` |
| `part` | string | part | `空间音效` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭声场模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "page": "设置",
        "object": "整车",
        "part": "空间音效",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭声场模式设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "page": "设置",
        "object": "整车",
        "part": "空间音效",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭智能声场

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "设置",
        "object": "整车",
        "part": "空间音效",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 关闭空间音效

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object": "整车",
        "part": "空间音效",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 关闭空间音效设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "整车",
        "part": "空间音效",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
