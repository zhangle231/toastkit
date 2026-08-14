# -*- coding: utf-8 -*-
"""
ToastKit MCP Server
将 ToastKit 封装为 MCP 工具，供 AI 客户端通过 MCP 协议调用发送 Windows 富通知。

运行方式（stdio）：
    python toast_mcp_server.py

依赖：
    pip install mcp winsdk
"""
import json
from mcp.server.mcpserver import MCPServer

from toast_template import send_toast, DEFAULTS

server = MCPServer("ToastKit")


@server.tool()
def send_toast_tool(
    title: str = DEFAULTS["title"],
    message: str = DEFAULTS["message"],
    header_title: str = "",
    hero_image: str = "",
    inline_image: str = "",
    image_crop: str = "none",
    progress_value: str = "",
    progress_title: str = "",
    progress_status: str = "",
    attribution: str = "",
    actions_json: str = "[]",
    launch: str = "",
    audio: str = "default",
    audio_loop: bool = False,
    duration: str = "long",
    scenario: str = "default",
    priority: str = "default",
) -> str:
    """发送 Windows 富通知。

    Args:
        title: 通知标题
        message: 通知正文
        header_title: 顶部标题栏文字（空=不显示）
        hero_image: 顶部大图路径（file:/// 或 http://）
        inline_image: 正文图片路径
        image_crop: 图片裁剪方式: circle / round / none
        progress_value: 进度条值: 0~1 或 indeterminate(动画)
        progress_title: 进度条标题
        progress_status: 进度条状态文本
        attribution: 底部归属文本
        actions_json: 按钮列表 JSON 字符串，如 [{"label":"打开","launch":"https://x.com"}]
        launch: 点击通知默认跳转 URL
        audio: 音频: default / alarm / call / silent
        audio_loop: 是否循环播放
        duration: 显示时长: short / long
        scenario: 场景: default / reminder / alarm / incomingCall
        priority: 优先级: default / high

    Returns:
        发送结果描述
    """
    try:
        actions = json.loads(actions_json) if actions_json else []
    except json.JSONDecodeError as e:
        return f"actions_json 解析失败: {e}"

    overrides = {
        "title": title,
        "message": message,
        "header_title": header_title,
        "hero_image": hero_image,
        "inline_image": inline_image,
        "image_crop": image_crop,
        "progress_value": progress_value,
        "progress_title": progress_title,
        "progress_status": progress_status,
        "attribution": attribution,
        "actions": actions,
        "launch": launch,
        "audio": audio,
        "audio_loop": audio_loop,
        "duration": duration,
        "scenario": scenario,
        "priority": priority,
    }
    # 空字符串字段不覆盖默认值
    overrides = {k: v for k, v in overrides.items() if v not in ("", [])}

    send_toast(**overrides)
    return f"通知已发送: {title}"


if __name__ == "__main__":
    server.run(transport="stdio")
