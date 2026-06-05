from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path


class VLMAPIError(RuntimeError):
    pass


def generate_api_report(
    image_path: str | Path,
    instruction: str,
    evidence_summary: str,
    context: list[str],
    timeout: int = 120,
) -> str:
    """Call an OpenAI-compatible multimodal API.

    The default environment variable names are compatible with DashScope/Qwen
    style deployments, but the same adapter can point to any OpenAI-compatible
    vision endpoint.
    """
    api_key = os.getenv("VLM_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise VLMAPIError("Missing VLM_API_KEY or DASHSCOPE_API_KEY.")

    base_url = os.getenv("VLM_API_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    model = os.getenv("VLM_API_MODEL", "qwen-vl-plus")
    endpoint = base_url.rstrip("/") + "/chat/completions"

    image_data_url = _image_to_data_url(image_path)
    prompt = _build_prompt(instruction, evidence_summary, context)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise VLMAPIError(f"VLM API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise VLMAPIError(f"VLM API connection failed: {exc}") from exc

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise VLMAPIError(f"Unexpected VLM API response: {data}") from exc

    if isinstance(content, list):
        return "\n".join(part.get("text", "") for part in content if isinstance(part, dict))
    return str(content)


def _image_to_data_url(path: str | Path) -> str:
    image_path = Path(path)
    suffix = image_path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _build_prompt(instruction: str, evidence_summary: str, context: list[str]) -> str:
    context_text = "\n".join(f"- {item}" for item in context)
    return f"""你是遥感智能解译算法工程师。请根据变化检测 overlay 图、用户任务和证据摘要，输出中文结构化分析报告。

重要约束：
- 必须优先相信“算法证据摘要”和“主要变化区域比例”，不要把变化比例为 0 的区域描述为主要变化区。
- overlay 图中的红色区域表示算法检测到的变化候选区；非红色区域只能作为背景描述。
- 不要声称已经确认“新建、拆除、灾害原因”等因果结论，只能写“疑似、可能、需要进一步验证”。
- 如果图像内容与算法证据不一致，请明确说明“不确定性”，不要强行下结论。

用户任务：
{instruction}

算法证据摘要：
{evidence_summary}

领域知识：
{context_text}

请严格按以下结构输出：
1. 变化概述
2. 主要变化区域
3. 可能的地物类型
4. 不确定性和误检风险
5. 下一步建议
"""
