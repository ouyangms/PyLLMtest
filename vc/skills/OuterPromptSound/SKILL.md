---
name: OuterPromptSound
description: Close external low speed prompt sound (关闭车外低速提示音)
---

## 功能说明
- 关闭车外低速提示音
- 车外低速提示音切换为初现
- 车外低速提示音切换为星火
- 车外低速提示音切换为流光
- 车外低速模拟音调节为银河音符/太空漫步/像素科技

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
        "feature": "车外低速模拟音",
        "action": "打开",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `车外低速模拟音` |
| `action` | string | action | `打开` |
| `object` | string | object | `整车` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭车外低速提示音

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "车外低速模拟音",
        "action": "关闭",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 开启车外低速提示音

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音效",
        "customInnerType": "nativeCommand",
        "action": "切换",
        "object": "整车",
        "sound": "银河音符",
        "feature": "车外低速模拟音",
        "action_concrete": "true"
    }
}
```

### 示例 3
**用户输入**: 车外低速提示音切换为像素科技

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音效",
        "customInnerType": "nativeCommand",
        "action": "切换",
        "object": "整车",
        "sound": "太空漫步",
        "feature": "车外低速模拟音",
        "action_concrete": "true"
    }
}
```

### 示例 4
**用户输入**: 车外低速提示音切换为初现

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音效",
        "customInnerType": "nativeCommand",
        "action": "切换",
        "object": "整车",
        "sound": "像素科技",
        "feature": "车外低速模拟音",
        "action_concrete": "true"
    }
}
```

### 示例 5
**用户输入**: 车外低速提示音切换为太空漫步

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音效",
        "customInnerType": "nativeCommand",
        "action": "切换",
        "object": "整车",
        "sound": "初现",
        "feature": "车外低速模拟音",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
