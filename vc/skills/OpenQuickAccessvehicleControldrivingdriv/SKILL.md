---
name: OpenQuickAccessvehicleControldrivingdriv
description: Open quick access|vehicle control|driving/driving control|light/light settings|assist driving/driving assist settings/page|voice/voice settings|display/display settings|sound|connection|my vehicle (打开快捷|车辆控制|驾驶/驾驶操控|灯光/灯光设置|辅助驾驶/驾驶辅助设置/页面|语音/语音设置|显示/显示设置|声音|连接|我的车辆)
---

## 功能说明
- 打开快捷|车辆控制|驾驶/驾驶操控|灯光/灯光设置|辅助驾驶/驾驶辅助设置/页面|语音/语音设置|显示/显示设置|声音|连接|我的车辆

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
        "function": "智慧巡航",
        "page": "设置",
        "subfunction": "辅助驾驶"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `智慧巡航` |
| `page` | string | page | `设置` |
| `subfunction` | string | subfunction | `辅助驾驶` |

## 调用示例

### 示例 1
**用户输入**: 打开声音设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page": "设置",
        "page_function": "我的车辆"
    }
}
```

### 示例 2
**用户输入**: 打开我的车辆设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page": "设置",
        "page_function": "驾驶操控",
        "object": "屏幕"
    }
}
```

### 示例 3
**用户输入**: 打开显示设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page": "设置",
        "object": "车灯"
    }
}
```

### 示例 4
**用户输入**: 打开灯光设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "智慧巡航",
        "page": "设置",
        "subfunction": "辅助驾驶"
    }
}
```

### 示例 5
**用户输入**: 打开语音设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "page": "设置",
        "module": "语音",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
