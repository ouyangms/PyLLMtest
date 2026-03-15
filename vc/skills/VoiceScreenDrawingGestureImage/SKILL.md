---
name: VoiceScreenDrawingGestureImage
description: Convert voice command to text and pass to AI graffiti to generate image (AI涂鸦使用过程中，在手势/屏幕涂鸦完成后的语音录入页将语音指令内容转化成文字透传给AI涂鸦，通过AI涂鸦算法解析生成图像)
---

## 功能说明
- AI涂鸦使用过程中，在手势/屏幕涂鸦完成后的语音录入页将语音指令内容转化成文字透传给AI涂鸦，通过AI涂鸦算法解析生成图像

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
