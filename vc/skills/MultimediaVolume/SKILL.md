---
name: MultimediaVolume
description: Close multimedia sound (关闭多媒体声音)
---

## 功能说明
- 关闭多媒体声音
- 关闭电台声音
- 关闭视频声音
- 关闭音乐声音
- 取消多媒体静音
- 取消电台静音
- 取消视频静音
- 取消音乐静音
- 多媒体减小3
- 多媒体声音大点
- 多媒体声音小点
- 多媒体静音
- 多媒体音量减小30%
- 多媒体音量增大3
- 多媒体音量增大30%
- 多媒体音量调到3
- 多媒体音量调到30%
- 多媒体音量调到最大
- 多媒体音量调到最小
- 打开多媒体声音
- 打开多媒体声音设置
- 打开电台声音
- 打开电台声音设置
- 打开视频声音
- 打开视频声音设置
- 打开音乐声音
- 打开音乐声音设置
- 电台声音大点
- 电台声音小点
- 电台静音
- 电台音量减小3
- 电台音量减小30%
- 电台音量增大3
- 电台音量增大30%
- 电台音量调到3
- 电台音量调到30%
- 电台音量调到最大
- 电台音量调到最小
- 视频声音大点
- 视频声音小点
- 视频静音
- 视频音量减小3
- 视频音量减小30%
- 视频音量增大3
- 视频音量增大30%
- 视频音量调到3
- 视频音量调到30%
- 视频音量调到最大
- 视频音量调到最小
- 音乐声音大点
- 音乐声音小点
- 音乐静音
- 音乐音量减小3
- 音乐音量减小30%
- 音乐音量增大3
- 音乐音量增大30%
- 音乐音量调到3
- 音乐音量调到30%
- 音乐音量调到最大
- 音乐音量调到最小

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
        "action": "关闭",
        "mode": "静音",
        "part": "模式",
        "module": "多媒体",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `mode` | string | mode | `静音` |
| `part` | string | part | `模式` |
| `module` | string | module | `多媒体` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `屏幕` |

## 调用示例

### 示例 1
**用户输入**: 关闭多媒体声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "静音",
        "part": "模式",
        "module": "音乐",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 2
**用户输入**: 关闭电台声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "静音",
        "part": "模式",
        "module": "电台",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 3
**用户输入**: 关闭视频声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "静音",
        "part": "模式",
        "module": "视频",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 4
**用户输入**: 关闭音乐声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "静音",
        "part": "模式",
        "module": "音乐",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 5
**用户输入**: 取消多媒体静音

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "静音",
        "part": "模式",
        "module": "电台",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
