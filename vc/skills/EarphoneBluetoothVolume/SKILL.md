---
name: EarphoneBluetoothVolume
description: Close Bluetooth earphone sound (关闭蓝牙耳机声音)
---

## 功能说明
- 关闭蓝牙耳机声音
- 关闭蓝牙耳机音量设置
- 打开蓝牙耳机声音
- 打开蓝牙耳机音量设置
- 蓝牙耳机取消静音
- 蓝牙耳机声音大点
- 蓝牙耳机声音小点
- 蓝牙耳机静音
- 蓝牙耳机音量减小3
- 蓝牙耳机音量减小30%
- 蓝牙耳机音量增大3
- 蓝牙耳机音量增大30%
- 蓝牙耳机音量调到3
- 蓝牙耳机音量调到30%
- 蓝牙耳机音量调到最大
- 蓝牙耳机音量调到最小

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
        "object_raw": "蓝牙耳机",
        "mode": "静音",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "蓝牙耳机"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `object_raw` | string | object_raw | `蓝牙耳机` |
| `mode` | string | mode | `静音` |
| `part` | string | part | `模式` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `蓝牙耳机` |

## 调用示例

### 示例 1
**用户输入**: 关闭蓝牙耳机声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "蓝牙耳机",
        "mode": "静音",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "蓝牙耳机"
    }
}
```

### 示例 2
**用户输入**: 关闭蓝牙耳机音量设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "蓝牙耳机",
        "mode": "静音",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object": "蓝牙耳机"
    }
}
```

### 示例 3
**用户输入**: 打开蓝牙耳机声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "mode": "静音",
        "part": "模式",
        "object": "蓝牙耳机"
    }
}
```

### 示例 4
**用户输入**: 打开蓝牙耳机音量设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "object_raw": "蓝牙耳机",
        "value": "+",
        "part_raw": "声音",
        "customInnerType": "nativeCommand",
        "object": "蓝牙耳机"
    }
}
```

### 示例 5
**用户输入**: 蓝牙耳机取消静音

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "object_raw": "蓝牙耳机",
        "value": "-",
        "part_raw": "声音",
        "customInnerType": "nativeCommand",
        "object": "蓝牙耳机"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
