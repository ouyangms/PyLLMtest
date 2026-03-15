---
name: ControlSideMirrorSentryFoldMode
description: Toggle side mirror sentry fold mode (后视镜哨兵折叠模式控制)
---

## 功能说明
- /

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
        "action": "关闭",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "mode": "哨兵",
        "page_function": "不折叠后视镜"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `part` | string | part | `模式` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `mode` | string | mode | `哨兵` |
| `page_function` | string | page_function | `不折叠后视镜` |

## 调用示例

### 示例 1
**用户输入**: 关闭哨兵模式不折叠后视镜

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "mode": "哨兵",
        "page_function": "不折叠后视镜"
    }
}
```

### 示例 2
**用户输入**: 关闭锁车保持后视镜展开功能

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "mode": "哨兵",
        "page_function": "不折叠后视镜"
    }
}
```

### 示例 3
**用户输入**: 哨兵模式不折叠后视镜

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "mode": "哨兵",
        "page_function": "不折叠后视镜"
    }
}
```

### 示例 4
**用户输入**: 哨兵模式保持折叠后视镜

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "mode": "哨兵",
        "page_function": "不折叠后视镜"
    }
}
```

### 示例 5
**用户输入**: 打开哨兵模式不折叠后视镜

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "mode": "哨兵",
        "page_function": "不折叠后视镜"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
