---
name: SteeringWheel
description: Close steering wheel assist settings (关闭方向盘助力设置)
---

## 功能说明
- 关闭方向盘助力设置
- 打开/关闭转向助力联动驾驶模式
- 打开方向盘助力设置
- 方向盘助力调到一挡
- 方向盘助力调到最高/最低
- 方向盘助力调高/调低点
- 转向助力设为舒适/标准/运动
- 转向模式调节为舒适/标准/运动

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
        "page": "设置",
        "feature": "助力",
        "object": "方向盘",
        "object_raw": "方向盘",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `page` | string | page | `设置` |
| `feature` | string | feature | `助力` |
| `object` | string | object | `方向盘` |
| `object_raw` | string | object_raw | `方向盘` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭方向盘助力设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "page": "设置",
        "feature": "助力",
        "object": "方向盘",
        "object_raw": "方向盘",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭转向助力

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "转动力度",
        "object": "方向盘",
        "customInnerType": "nativeCommand",
        "value": "1",
        "object_raw": "方向盘",
        "action_concrete": "true",
        "feature": "助力"
    }
}
```

### 示例 3
**用户输入**: 关闭转向助力联动驾驶模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "转动力度",
        "customInnerType": "nativeCommand",
        "object_raw": "方向盘",
        "value": "+",
        "object": "方向盘",
        "feature": "助力"
    }
}
```

### 示例 4
**用户输入**: 打开方向盘助力设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "转动力度",
        "customInnerType": "nativeCommand",
        "object_raw": "方向盘",
        "value": "-",
        "object": "方向盘",
        "feature": "助力"
    }
}
```

### 示例 5
**用户输入**: 打开转向助力

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "转动力度",
        "object": "方向盘",
        "customInnerType": "nativeCommand",
        "value": "max",
        "object_raw": "方向盘",
        "action_concrete": "true",
        "feature": "助力"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
