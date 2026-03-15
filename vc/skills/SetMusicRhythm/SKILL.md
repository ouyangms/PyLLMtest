---
name: SetMusicRhythm
description: Close tech belt music rhythm (关闭科技带音乐随动(音乐律动))
---

## 功能说明
- 关闭科技带音乐随动(音乐律动)
- 打开【数字光语】音乐随动(音乐律动)
- 打开数字光语的-旋律律动
- 打开数字光语的-歌词模式

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
        "mode": "旋律律动",
        "action": "打开",
        "object": "车外灯",
        "function": "灯语",
        "part": "模式"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `mode` | string | mode | `旋律律动` |
| `action` | string | action | `打开` |
| `object` | string | object | `车外灯` |
| `function` | string | function | `灯语` |
| `part` | string | part | `模式` |

## 调用示例

### 示例 1
**用户输入**: 关闭科技带的音乐随动

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "mode": "旋律律动",
        "action": "关闭",
        "object": "车外灯",
        "function": "灯语",
        "part": "模式"
    }
}
```

### 示例 2
**用户输入**: 打开数字光语的旋律律动

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "灯语",
        "mode": "歌词",
        "part": "模式",
        "object": "车外灯"
    }
}
```

### 示例 3
**用户输入**: 打开数字光语的歌词模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "灯语",
        "mode": "旋律律动",
        "part": "模式",
        "object": "车外灯"
    }
}
```

### 示例 4
**用户输入**: 打开数字光语的音乐律动

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "mode": "旋律律动",
        "action": "打开",
        "object": "车外灯",
        "function": "灯语",
        "part": "模式"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
