---
name: QueryCurrentAirflowAirConditioner
description: Front row/driver/passenger/left front/right front first row = first row air conditioner (前排/主驾/副驾/左前/右前第一排=一排空调)
---

## 功能说明
- 前排/主驾/副驾/左前/右前第一排=一排空调

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
        "part": "风力",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "object": "空调"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `风力` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `查看` |
| `object` | string | object | `空调` |

## 调用示例

### 示例 1
**用户输入**: 现在二排空调风量是几挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "风力",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "object": "空调",
        "position": "第二排"
    }
}
```

### 示例 2
**用户输入**: 现在空调风量是几挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "风力",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "object": "空调"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
