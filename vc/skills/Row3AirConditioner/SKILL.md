---
name: Row3AirConditioner
description: Toggle third row air conditioner (控制车辆三排空调功能)
---

## 功能说明
- 控制车辆三排空调功能

## 调用逻辑
1. **意图解析**：系统自动识别用户指令中的操作意图和参数
2. **参数提取**：从用户自然语言中提取相关参数
3. **工具调用**：调用车辆控制工具执行相应操作

## 参数规范
用户输入自然语言指令后，LLM 需要提取参数并输出以下格式：

```json
{
    "api": "sys.car.crl",
    "param": {}
}
```


## 调用示例

### 示例 1
**用户输入**: /

```json
{
    "api": "sys.car.crl",
    "param": {}
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
