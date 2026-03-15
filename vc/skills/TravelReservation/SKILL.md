---
name: TravelReservation
description: Close cabin comfort (关闭座舱舒适)
---

## 功能说明
- 关闭座舱舒适
- 关闭电池维温
- 关闭预约出行
- 关闭预约出行电池预热
- 关闭预约出行页面
- 打开座舱舒适
- 打开电池维温
- 打开预约出行
- 打开预约出行电池预热
- 打开预约出行页面
- 设置预约出行时间
- 预约出行日期为周一
- 预约出行日期为周三
- 预约出行日期为周二
- 预约出行日期为周五
- 预约出行日期为周六
- 预约出行日期为周四
- 预约出行日期为周日
- 预约出行时间为13点

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
        "customInnerType": "nativeCommand",
        "function": "预约出行",
        "page": "页面"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `预约出行` |
| `page` | string | page | `页面` |

## 调用示例

### 示例 1
**用户输入**: 关闭座舱舒适

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "预约出行",
        "page": "页面"
    }
}
```

### 示例 2
**用户输入**: 关闭电池维温

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "function": "预约出行"
    }
}
```

### 示例 3
**用户输入**: 关闭预约出行

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "function": "预约出行"
    }
}
```

### 示例 4
**用户输入**: 关闭预约出行电池预热

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "日期",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "function": "预约出行",
        "value": "周一"
    }
}
```

### 示例 5
**用户输入**: 关闭预约出行页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "日期",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "function": "预约出行",
        "value": "周二"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
