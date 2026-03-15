---
name: SoundEffect
description: Play tiger/lion/cat/whistle/hawker/super engine/tractor/old village chief sound (播放老虎声/狮子声/猫咪声/口哨声/叫卖声/超跑引擎/拖拉机/老村长)
---

## 功能说明
- 播放老虎声/狮子声/猫咪声/口哨声/叫卖声/超跑引擎/拖拉机/老村长

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

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|

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
