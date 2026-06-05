from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from .change_detection import detect_changes
from .reporting import build_markdown_report
from .retrieval import retrieve_knowledge
from .vlm_api import VLMAPIError, generate_api_report


@dataclass
class ChangeEvidence:
    changed_ratio: float
    confidence: str
    key_regions: list[str]
    mask_path: str | None = None
    overlay_path: str | None = None


@dataclass
class AgentReport:
    task: str
    summary: str
    evidence: ChangeEvidence
    recommendations: list[str]
    model_mode: str
    retrieved_context: list[str]
    markdown_report: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = asdict(self.evidence)
        return data


def analyze_scene(
    pre_image: str | Path,
    post_image: str | Path,
    instruction: str,
    model_mode: str = "heuristic",
    output_dir: str | Path = "outputs",
) -> AgentReport:
    """Analyze a remote-sensing scene with a replaceable VLM backend.

    The current implementation is intentionally lightweight. It validates the
    workflow shape and provides stable outputs before heavier model adapters are
    connected.
    """
    pre_path = Path(pre_image)
    post_path = Path(post_image)
    if not pre_path.exists():
        raise FileNotFoundError(f"Pre-event image not found: {pre_path}")
    if not post_path.exists():
        raise FileNotFoundError(f"Post-event image not found: {post_path}")

    instruction_lower = instruction.lower()
    focus = "building and land-cover change"
    if "road" in instruction_lower or "道路" in instruction:
        focus = "road and transportation change"
    elif "water" in instruction_lower or "水体" in instruction:
        focus = "water-body and shoreline change"
    elif "building" in instruction_lower or "建筑" in instruction:
        focus = "building change"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    change_result = detect_changes(pre_path, post_path, output_path)
    context = retrieve_knowledge(instruction, top_k=3)

    evidence = ChangeEvidence(
        changed_ratio=change_result.changed_ratio,
        confidence=change_result.confidence,
        key_regions=change_result.region_descriptions,
        mask_path=str(change_result.mask_path),
        overlay_path=str(change_result.overlay_path),
    )

    evidence_summary = (
        f"The agent analyzed pre/post remote-sensing images with a focus on "
        f"{focus}. Estimated changed area ratio is "
        f"{change_result.changed_ratio:.2%}, with {change_result.confidence} "
        f"confidence from the lightweight image backend. Region evidence: "
        f"{'; '.join(change_result.region_descriptions)}."
    )
    summary = evidence_summary
    if model_mode in {"api", "qwen_api", "dashscope"}:
        try:
            summary = generate_api_report(
                change_result.overlay_path,
                instruction,
                evidence_summary,
                context,
            )
        except VLMAPIError as exc:
            summary = (
                f"{evidence_summary}\n\nAPI mode was requested, but the VLM call "
                f"did not complete: {exc}"
            )

    recommendations = [
        "Review the overlay visualization before using the report for decisions.",
        "Use a supervised change-detection model for production-grade masks.",
        "Connect Qwen-VL or InternVL when visual-language explanations are needed.",
    ]

    report = AgentReport(
        task=instruction,
        summary=summary,
        evidence=evidence,
        recommendations=recommendations,
        model_mode=model_mode,
        retrieved_context=context,
        markdown_report="",
    )
    report.markdown_report = build_markdown_report(report)
    (output_path / "report.md").write_text(report.markdown_report, encoding="utf-8")
    return report
