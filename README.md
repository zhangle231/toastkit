---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4ff5be3e1f50ff475cd88e8c986c75f_02ee4fe9979211f1b995525400e6dd8f
    ReservedCode1: 41RAHWYZiH1rciCP3eCOlL5EZbr3cqh+qUin2Y+7hvic4qh8IoTbuTO1+gFfdZFgoXxAKJfiNCAE3zgOyyMxKyu8qTSHc3TwupHviZFLeVClfuU1NYwLQ3pJKiW55JQndREbtMMs/s8JZT2hte+QVudZMkLDeFWJiVoZYR2fnenb3kLpYDnrZGzbX0A=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4ff5be3e1f50ff475cd88e8c986c75f_02ee4fe9979211f1b995525400e6dd8f
    ReservedCode2: 41RAHWYZiH1rciCP3eCOlL5EZbr3cqh+qUin2Y+7hvic4qh8IoTbuTO1+gFfdZFgoXxAKJfiNCAE3zgOyyMxKyu8qTSHc3TwupHviZFLeVClfuU1NYwLQ3pJKiW55JQndREbtMMs/s8JZT2hte+QVudZMkLDeFWJiVoZYR2fnenb3kLpYDnrZGzbX0A=
---

# ToastKit

Windows 全功能富通知模板，基于原生 Toast XML，一行代码发送高定制化系统通知。

## 功能特性

- 顶部标题栏（header）
- 顶部大图（hero image）
- 正文图片 + 圆形裁剪（hint-crop）
- 进度条：静态值（0~1）或动画（indeterminate）
- 底部归属文本（attribution）
- 多按钮（打开链接 / 系统关闭）
- 循环声音（默认 / 闹钟 / 来电）
- 高优先级置顶
- 自定义应用名（AUMID）

## 环境要求

- Windows 10/11
- Python 3.8+
- `pip install winsdk`

## 快速开始

```python
from toast_template import send_toast

# 默认效果（全功能演示版）
send_toast()

# 自定义内容
send_toast(
    title="下载完成",
    message="文件已保存到桌面",
    progress_value=1.0,
    audio="default",
    audio_loop=False,
)
```

## 字段说明

| 字段 | 说明 | 默认值 |
|---|---|---|
| `app_id` | 应用名（AUMID） | `Marvis.Notification` |
| `title` | 通知标题 | 必填 |
| `message` | 通知正文 | 必填 |
| `header_title` | 顶部标题栏 | 空 |
| `hero_image` | 顶部大图路径 | 空 |
| `inline_image` | 正文图片路径 | 空 |
| `image_crop` | 图片裁剪（circle/round/none） | none |
| `progress_value` | 进度条（0~1 或 indeterminate） | 空 |
| `progress_title` | 进度条标题 | 空 |
| `progress_status` | 进度条状态文本 | 空 |
| `attribution` | 底部归属文本 | 空 |
| `actions` | 按钮列表 [{label, launch}] | 空 |
| `launch` | 点击通知默认跳转 | 空 |
| `audio` | 音频（default/alarm/call/silent） | default |
| `audio_loop` | 是否循环播放 | false |
| `duration` | 显示时长（short/long） | long |
| `scenario` | 场景（default/reminder/alarm/incomingCall） | default |
| `priority` | 优先级（default/high） | default |

## 自定义 AUMID

默认使用 `Marvis.Notification`，需在注册表注册应用名与图标：

```
HKCU\Software\Classes\AppUserModelId\Marvis.Notification
  DisplayName = "Marvis 通知"
  IconUri = <图标路径>
```

## 命令行运行

```powershell
python toast_template.py
```

## MCP 接口

ToastKit 提供 MCP server，AI 客户端可通过 MCP 协议直接调用发送通知。

### 启动

```powershell
python toast_mcp_server.py
```

### 工具

- `send_toast_tool`：发送富通知，参数与模板字段一致（`actions_json` 为按钮列表 JSON 字符串）

### 客户端配置示例（Claude Desktop）

```json
{
  "mcpServers": {
    "toastkit": {
      "command": "python",
      "args": ["D:/LEO/project/temp/toastkit/toast_mcp_server.py"]
    }
  }
}
```

### 依赖

```powershell
pip install mcp winsdk
```

## License

MIT
*（内容由AI生成，仅供参考）*
