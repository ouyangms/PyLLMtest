---
name: OpenSuspensionEasyLoadingMode
description: Open suspension easy loading mode (控制车辆打开悬架轻松载物模式功能)
---

## 功能说明
- 控制车辆打开悬架轻松载物模式功能

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
        "object_raw": "悬架",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "悬架",
        "part": "模式",
        "mode": "轻松载物",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object_raw` | string | object_raw | `悬架` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part_raw` | string | part_raw | `模式` |
| `object` | string | object | `悬架` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `轻松载物` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 打开悬架轻松载物模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "悬架",
        "part": "模式",
        "mode": "轻松载物",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
