---
name: OpenRow2UpGesture
description: Open second row screen gesture back tutorial (打开二排屏手势返回上一页教学)
---

## 功能说明
- 打开二排屏手势返回上一页教学

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
        "subfunction": "返回上一页教程"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `手势教学引导` |
| `subfunction` | string | subfunction | `返回上一页教程` |

## 调用示例

### 示例 1
**用户输入**: xxxx=返回上一页/退出/退出当

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "手势教学引导",
        "subfunction": "返回上一页教程"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
