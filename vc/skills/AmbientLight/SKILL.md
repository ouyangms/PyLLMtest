---
name: AmbientLight
description: Open music rhythm ambient light at [location] ([location]打开音乐律动氛围灯)
---

## 功能说明
- 【位置】打开音乐律动氛围灯
- 亮度极值调节
- 亮度相对值调节
- 亮度绝对值调节（1-20，默认10级）
- 关闭
- 关闭主题色模式氛围灯
- 关闭双色氛围灯
- 关闭呼吸氛围灯
- 关闭屏幕取色氛围灯
- 关闭心跳氛围灯
- 关闭时光引擎氛围灯
- 关闭氛围灯
- 关闭续航报警氛围灯
- 关闭转向联动氛围灯
- 切换呼吸氛围灯速度/快/慢
- 切换心跳氛围灯速度/快/慢
- 切换氛围灯为主题色模式
- 切换氛围灯为屏幕取色模式
- 切换氛围灯为时光引擎模式
- 切换氛围灯为自定义模式（自定义模式包含：纯色、呼吸、双色、心跳）
- 切换氛围灯为驾驶联动模式（常态显示）
- 切换氛围灯主题色模式
- 切换（位置）氛围灯颜色为红色
- 我想要10号色氛围灯（共64色）
- 打开
- 打开/关闭
- 打开/关闭子选项：上车迎宾、续航提醒、来电律动/来电提醒、空调联动/空调温度调节、语音助手、音乐律动
- 打开/关闭氛围灯颜色设置页
- 打开/关闭（位置）氛围灯
- 打开主题色模式氛围灯
- 打开双色氛围灯
- 打开呼吸氛围灯
- 打开屏幕取色氛围灯
- 打开心跳氛围灯
- 打开时光引擎氛围灯
- 打开氛围灯
- 打开氛围灯设置
- 打开续航报警氛围灯
- 打开转向联动氛围灯
- 换一个氛围灯颜色
- 氛围灯颜色（红、橙、黄、绿、青、蓝、紫、粉）常用色（黄色/金色/辣芥末黄
- 设置为双色交替
- 设置为呼吸|渐变（名字可能会变）
- 设置为纯色模式
- 设置为自定义/驾驶/天气/语音
- 设置为驾驶联动
- （位置）换一个氛围灯颜色

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
        "object_raw": "氛围灯",
        "customInnerType": "nativeCommand",
        "light_type_inside": "氛围灯",
        "object": "车内灯"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `氛围灯` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `light_type_inside` | string | light_type_inside | `氛围灯` |
| `object` | string | object | `车内灯` |

## 调用示例

### 示例 1
**用户输入**: 主驾打开音乐律动氛围灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "氛围灯",
        "object": "车内灯",
        "light_type_inside": "氛围灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关掉氛围灯随音乐跳动

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "氛围灯",
        "customInnerType": "nativeCommand",
        "light_type_inside": "氛围灯",
        "object": "车内灯"
    }
}
```

### 示例 3
**用户输入**: 关闭上车迎宾氛围灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "light_type_outside": "位置灯",
        "customInnerType": "nativeCommand",
        "object": "车外灯",
        "object_raw": "位置灯",
        "action": "打开",
        "position": "副驾"
    }
}
```

### 示例 4
**用户输入**: 关闭主题色模式氛围灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "light_type_outside": "位置灯",
        "customInnerType": "nativeCommand",
        "object": "车外灯",
        "object_raw": "位置灯",
        "action": "关闭",
        "position": "副驾"
    }
}
```

### 示例 5
**用户输入**: 关闭副驾位置灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "车内灯",
        "part": "模式",
        "mode": "驾驶联动",
        "light_type_inside": "氛围灯",
        "customInnerType": "nativeCommand",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
