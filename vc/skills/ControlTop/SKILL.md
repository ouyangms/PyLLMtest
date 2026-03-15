---
name: ControlTop
description: Close roof light (关闭车顶灯)
---

## 功能说明
- 关闭车顶灯
- 关闭车顶灯设置
- 打开车顶灯
- 打开车顶灯设置

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
        "object_raw": "顶灯",
        "customInnerType": "nativeCommand",
        "light_type_inside": "车顶灯",
        "object": "车内灯"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `顶灯` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `light_type_inside` | string | light_type_inside | `车顶灯` |
| `object` | string | object | `车内灯` |

## 调用示例

### 示例 1
**用户输入**: 关闭内部灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "内部灯",
        "object": "车内灯",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭照明

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "照明",
        "object": "车内灯",
        "light_type_inside": "车顶灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭车顶灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "顶灯",
        "customInnerType": "nativeCommand",
        "light_type_inside": "车顶灯",
        "object": "车内灯"
    }
}
```

### 示例 4
**用户输入**: 关闭车顶灯设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "内部灯",
        "object": "车内灯",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 打开内部灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "照明",
        "object": "车内灯",
        "light_type_inside": "车顶灯",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
