from __future__ import annotations

from pathlib import Path

import gradio as gr

from src.rs_vlm_agent import analyze_scene


def run_agent(pre_image: str, post_image: str, instruction: str, model_mode: str):
    report = analyze_scene(
        pre_image,
        post_image,
        instruction,
        model_mode=model_mode,
        output_dir="outputs/gradio",
    )
    overlay = report.evidence.overlay_path
    metrics = {
        "changed_ratio": f"{report.evidence.changed_ratio:.2%}",
        "confidence": report.evidence.confidence,
        "key_regions": report.evidence.key_regions,
        "mask_path": report.evidence.mask_path,
        "overlay_path": report.evidence.overlay_path,
        "model_mode": report.model_mode,
    }
    return overlay, report.markdown_report, metrics, report.evidence.mask_path


EXAMPLES = [
    [
        "demo_data/pre.png",
        "demo_data/post.png",
        "请严格依据算法证据分析这组遥感影像中的建筑和道路变化，并给出结构化中文报告。不要把变化比例为0的区域描述为主要变化区。",
        "qwen_api",
    ],
    [
        "demo_data/pre.png",
        "demo_data/post.png",
        "Analyze building and road changes with uncertainty notes.",
        "heuristic",
    ],
    [
        "real_cases/case_001_sysu_cd_00071/pre.png",
        "real_cases/case_001_sysu_cd_00071/post.png",
        "请分析 SYSU-CD 真实样本中的变化区域，并说明不确定性。",
        "heuristic",
    ],
    [
        "real_cases/case_002_dsifn_46/pre.jpg",
        "real_cases/case_002_dsifn_46/post.jpg",
        "请分析 DSIFN 真实样本中的变化区域，并说明可能的误检风险。",
        "heuristic",
    ],
    [
        "real_cases/case_003_cdd_svcd_0272/pre.jpg",
        "real_cases/case_003_cdd_svcd_0272/post.jpg",
        "请分析 CDD/SVCD 真实样本中的变化区域，并给出后续验证建议。",
        "heuristic",
    ],
]


with gr.Blocks(title="GeoVLM-ChangeAgent", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
# GeoVLM-ChangeAgent

Upload a pre-event and post-event remote-sensing image pair. The system computes
a lightweight change mask, overlays visual evidence, retrieves domain knowledge,
and generates a structured report with either local heuristic mode or Qwen/API mode.

Mode guide:

- `heuristic`: local CPU mode. No API key is required.
- `qwen_api`: Qwen-VL report mode. Set `DASHSCOPE_API_KEY` before starting the app.
"""
    )
    with gr.Row():
        with gr.Column(scale=1):
            pre = gr.Image(type="filepath", label="Pre-event image", height=260)
            post = gr.Image(type="filepath", label="Post-event image", height=260)
        with gr.Column(scale=1):
            instruction = gr.Textbox(
                label="Instruction",
                value="请严格依据算法证据分析这组遥感影像中的建筑和道路变化，并给出结构化中文报告。不要把变化比例为0的区域描述为主要变化区。",
                lines=4,
            )
            model_mode = gr.Dropdown(
                choices=["heuristic", "api", "qwen_api", "dashscope"],
                value="heuristic",
                label="Model mode",
            )
            run = gr.Button("Analyze", variant="primary")

    with gr.Row():
        overlay = gr.Image(type="filepath", label="Change overlay", height=360)
        mask = gr.Image(type="filepath", label="Binary change mask", height=360)

    with gr.Row():
        metrics = gr.JSON(label="Evidence metrics")

    report = gr.Markdown(label="Structured report")

    gr.Examples(
        examples=EXAMPLES,
        inputs=[pre, post, instruction, model_mode],
        label="Demo examples",
    )

    run.click(
        run_agent,
        inputs=[pre, post, instruction, model_mode],
        outputs=[overlay, report, metrics, mask],
    )


if __name__ == "__main__":
    Path("outputs/gradio").mkdir(parents=True, exist_ok=True)
    Path("demo_data").mkdir(parents=True, exist_ok=True)
    demo.launch(server_name="127.0.0.1", server_port=7860)
