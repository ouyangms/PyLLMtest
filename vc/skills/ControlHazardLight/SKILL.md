---
name: ControlHazardLight
description: Close hazard light (关闭双闪)
---

## 功能说明
- 关闭双闪
- 打开双闪

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
        "light_type_outside": "警示灯",
        "action": "打开",
        "object_raw": "双闪",
        "object": "车外灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `light_type_outside` | string | light_type_outside | `警示灯` |
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `双闪` |
| `object` | string | object | `车外灯` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭双闪

```json
{
    "api": "sys.car.crl",
    "param": {
        "light_type_outside": "警示灯",
        "action": "关闭",
        "object_raw": "双闪",
        "object": "车外灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开双闪

```json
{
    "api": "sys.car.crl",
    "param": {
        "light_type_outside": "警示灯",
        "action": "打开",
        "object_raw": "双闪",
        "object": "车外灯",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
