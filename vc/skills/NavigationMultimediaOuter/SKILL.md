---
name: NavigationMultimediaOuter
description: Unmute multimedia/navigation/external speaker (控制车辆取消多媒体/导航/车外扬声器静音功能)
---

## 功能说明
- 控制车辆取消多媒体/导航/车外扬声器静音功能

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
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action": "关闭",
        "position": "all",
        "part": "模式",
        "mode": "静音"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `屏幕` |
| `action` | string | action | `关闭` |
| `position` | string | position | `all` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `静音` |

## 调用示例

### 示例 1
**用户输入**: 取消全车静音

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "action": "关闭",
        "position": "all",
        "part": "模式",
        "mode": "静音"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
