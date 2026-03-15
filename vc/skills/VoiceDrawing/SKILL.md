---
name: VoiceDrawing
description: Convert voice command to text and pass to AI album to generate image (通过语音指令"我要画……"将语音指令内容转化成文字透传给AI相册，通过AI相册算法解析生成图像)
---

## 功能说明
- 通过语音指令“我要画……”将语音指令内容转化成文字透传给AI相册，通过AI相册算法解析生成图像

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
