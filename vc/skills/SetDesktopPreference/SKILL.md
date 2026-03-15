---
name: SetDesktopPreference
description: Close desktop preference (关闭桌面偏好)
---

## 功能说明
- 关闭桌面偏好
- 换个桌面偏好
- 桌面偏好切换【地图】
- 桌面偏好切换【壁纸】
- 桌面偏好切换【实况】

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
        "action": "切换",
        "part": "模式",
        "mode": "实况",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `切换` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `实况` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `屏幕` |
| `action_concrete` | string | action_concrete | `true` |

## 调用示例

### 示例 1
**用户输入**: 关闭桌面偏好

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "part": "模式",
        "mode": "地图",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true"
    }
}
```

### 示例 2
**用户输入**: 切换成壁纸桌面

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "part": "模式",
        "mode": "壁纸",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true"
    }
}
```

### 示例 3
**用户输入**: 换个桌面模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "part": "模式",
        "mode": "壁纸",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action_concrete": "true"
    }
}
```

### 示例 4
**用户输入**: 桌面偏好切换为地图

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "function": "桌面偏好",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 5
**用户输入**: 桌面偏好切换为壁纸

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "function": "桌面偏好",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
