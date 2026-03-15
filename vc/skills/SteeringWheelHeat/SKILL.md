---
name: SteeringWheelHeat
description: Toggle steering wheel heating (打开/关闭方向盘加热)
---

## 功能说明
- 打开/关闭方向盘加热
- 打开/关闭方向盘加热设置
- 打开/关闭方向盘自动加热
- 方向盘加热开到2挡
- 方向盘加热开到最大/最小
- 方向盘加热开大/开小一点

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
        "feature": "加热",
        "customInnerType": "nativeCommand",
        "object_raw": "方向盘",
        "object": "方向盘"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `feature` | string | feature | `加热` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object_raw` | string | object_raw | `方向盘` |
| `object` | string | object | `方向盘` |

## 调用示例

### 示例 1
**用户输入**: 关闭方向盘加热

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "feature": "加热",
        "customInnerType": "nativeCommand",
        "object_raw": "方向盘",
        "object": "方向盘"
    }
}
```

### 示例 2
**用户输入**: 关闭方向盘加热设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "方向盘",
        "mode": "自动",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "feature": "加热",
        "object": "方向盘"
    }
}
```

### 示例 3
**用户输入**: 关闭方向盘自动加热

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "方向盘",
        "mode": "自动",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "feature": "加热",
        "object": "方向盘"
    }
}
```

### 示例 4
**用户输入**: 打开方向盘加热

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "page": "设置",
        "feature": "加热",
        "object": "方向盘",
        "object_raw": "方向盘",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 打开方向盘加热设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "设置",
        "feature": "加热",
        "object": "方向盘",
        "object_raw": "方向盘",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
