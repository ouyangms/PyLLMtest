---
name: ToggleDolbyPanoramicSound
description: Toggle Dolby panoramic sound (打开/关闭杜比全景声)
---

## 功能说明
- 打开/关闭杜比全景声
- 把杜比全景声控制界面/控制页面打开/关闭

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
        "customInnerType": "nativeCommand",
        "action": "打开",
        "feature": "杜比全景声",
        "object": "整车"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `feature` | string | feature | `杜比全景声` |
| `object` | string | object | `整车` |

## 调用示例

### 示例 1
**用户输入**: 关闭杜比全景声

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "feature": "杜比全景声",
        "object": "整车"
    }
}
```

### 示例 2
**用户输入**: 打开杜比音效

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page": "设置",
        "feature": "杜比全景声",
        "object": "整车"
    }
}
```

### 示例 3
**用户输入**: 把杜比全景声控制界面打开

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "page": "设置",
        "feature": "杜比全景声",
        "object": "整车"
    }
}
```

### 示例 4
**用户输入**: 把杜比全景声控制页面关闭

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "feature": "杜比全景声",
        "object": "整车"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
