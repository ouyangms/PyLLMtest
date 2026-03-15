---
name: SetAirVentMode
description: Set [zone] air vent mode (控制车辆[zone]设置出风口模式功能)
---

## 功能说明
- 控制车辆【音区】设置出风口模式功能

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
        "action_concrete": "true",
        "part": "模式",
        "mode": "手动",
        "feature": "出风口",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "空调"
    }
}
```

### 特殊参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `zone` | string | 音区参数（主驾音区/副驾音区/全车/一排/二排/三排） | `主驾音区` |

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action_concrete` | string | action_concrete | `true` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `手动` |
| `feature` | string | feature | `出风口` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part_raw` | string | part_raw | `模式` |
| `object` | string | object | `空调` |

## 调用示例

### 示例 1
**用户输入**: 出风口设置为上下扫风模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "part": "模式",
        "mode": "普通",
        "feature": "出风口",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "空调"
    }
}
```

### 示例 2
**用户输入**: 出风口设置为左右扫风模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "part": "模式",
        "mode": "聚焦",
        "feature": "出风口",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "空调"
    }
}
```

### 示例 3
**用户输入**: 出风口设置为手动模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "part": "模式",
        "mode": "避开",
        "feature": "出风口",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "空调"
    }
}
```

### 示例 4
**用户输入**: 出风口设置为摆动模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "part": "风向",
        "feature": "出风口",
        "customInnerType": "nativeCommand",
        "value": "左右循环",
        "object": "空调"
    }
}
```

### 示例 5
**用户输入**: 出风口设置为普通模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "part": "模式",
        "mode": "摆风",
        "feature": "出风口",
        "customInnerType": "nativeCommand",
        "object": "空调"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
