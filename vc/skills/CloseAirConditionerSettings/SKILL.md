---
name: CloseAirConditionerSettings
description: Close second row air conditioner settings (关闭二排空调设置)
---

## 功能说明
- 关闭二排空调设置

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
        "page": "设置",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "空调",
        "position": "第二排"
    }
}
```

### 特殊参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `position` | string | 位置参数（主驾/副驾/一排/二排/三排/前排/后排/全车） | `主驾` |

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `page` | string | page | `设置` |
| `object_raw` | string | object_raw | `空调` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `关闭` |
| `object` | string | object | `空调` |
| `position` | string | position | `第二排` |

## 调用示例

### 示例 1
**用户输入**: 关闭二排空调设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "空调",
        "position": "第二排"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
