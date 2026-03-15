---
name: OpenUpDownLeftRightRow2Gesture
description: Open second row screen gesture up/down/left/right page tutorial (打开二排屏手势上下左右翻页教学)
---

## 功能说明
- 打开二排屏手势上下左右翻页教学

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
        "function": "手势教学引导",
        "subfunction": "上下左右翻页教学"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `手势教学引导` |
| `subfunction` | string | subfunction | `上下左右翻页教学` |

## 调用示例

### 示例 1
**用户输入**: 1.手势怎么控制上下翻页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "手势教学引导",
        "subfunction": "上下左右翻页教学"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
