---
name: SwitchLaneDepartureWarningMode
description: Switch lane departure warning mode (控制车辆车道偏离预警方式切换功能)
---

## 功能说明
- 控制车辆车道偏离预警方式切换功能

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
        "subfunction": "车道偏离",
        "function": "车道辅助",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `subfunction` | string | subfunction | `车道偏离` |
| `function` | string | function | `车道辅助` |
| `action` | string | action | `关闭` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 车道偏离预警方式为声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "声音",
        "part_raw": "预警方式",
        "subfunction": "车道偏离",
        "part": "预警方式",
        "function": "车道辅助",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 车道偏离预警方式为无预警

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "方向盘振动",
        "part_raw": "预警方式",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "车道辅助",
        "subfunction": "车道偏离",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 车道偏离预警方式设置为方向盘震动

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "车道偏离",
        "function": "车道辅助",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
