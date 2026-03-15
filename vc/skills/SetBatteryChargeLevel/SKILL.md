---
name: SetBatteryChargeLevel
description: Set battery hold level to target (将电量保持值设置为目标值)
---

## 功能说明
- 将电量保持值设置为目标值
- 打开/关闭保电与补电
- 打开/关闭燃油补电
- 设置电量保持值最大
- 设置电量保持值最小

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
        "function": "保电与补电",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `保电与补电` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭保电与补电页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "保电与补电",
        "action": "关闭",
        "page": "页面"
    }
}
```

### 示例 2
**用户输入**: 关闭燃油补电

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "电量保持值",
        "value": "50/100",
        "action_concrete": "true",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 打开保电与补电

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "电量保持值",
        "value": "max",
        "action_concrete": "true",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开燃油补电

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "电量保持值",
        "value": "min",
        "action_concrete": "true",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 把电量保持值调到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "function": "燃油补电"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
