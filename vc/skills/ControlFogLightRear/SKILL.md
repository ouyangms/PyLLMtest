---
name: ControlFogLightRear
description: Close rear fog light (关闭后雾灯)
---

## 功能说明
- 关闭后雾灯
- 关闭后雾灯设置页
- 打开后雾灯
- 打开后雾灯设置页

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
        "object_raw": "雾灯",
        "customInnerType": "nativeCommand",
        "position": "后",
        "light_type_outside": "雾灯",
        "object": "车外灯"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `雾灯` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `position` | string | position | `后` |
| `light_type_outside` | string | light_type_outside | `雾灯` |
| `object` | string | object | `车外灯` |

## 调用示例

### 示例 1
**用户输入**: 关闭后雾灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "后",
        "light_type_outside": "雾灯",
        "object_raw": "雾灯",
        "object": "车外灯",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭后雾灯设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "light_type_outside": "雾灯",
        "object_raw": "雾灯",
        "object": "车外灯",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 帮我打开后雾灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "雾灯",
        "customInnerType": "nativeCommand",
        "position": "后",
        "light_type_outside": "雾灯",
        "object": "车外灯"
    }
}
```

### 示例 4
**用户输入**: 打开后雾灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "雾灯",
        "customInnerType": "nativeCommand",
        "light_type_outside": "雾灯",
        "position": "后",
        "page": "设置",
        "object": "车外灯"
    }
}
```

### 示例 5
**用户输入**: 打开后雾灯设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "雾灯",
        "customInnerType": "nativeCommand",
        "light_type_outside": "雾灯",
        "position": "后",
        "page": "设置",
        "object": "车外灯"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
