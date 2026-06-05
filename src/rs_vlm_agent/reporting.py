from __future__ import annotations

from typing import Protocol


class ReportLike(Protocol):
    task: str
    summary: str
    recommendations: list[str]
    retrieved_context: list[str]
    evidence: object


def build_markdown_report(report: ReportLike) -> str:
    evidence = report.evidence
    lines = [
        "# GeoVLM-ChangeAgent Report",
        "",
        f"## Task",
        report.task,
        "",
        "## Summary",
        report.summary,
        "",
        "## Visual Evidence",
        f"- Changed ratio: {getattr(evidence, 'changed_ratio'):.2%}",
        f"- Confidence: {getattr(evidence, 'confidence')}",
        f"- Mask: {getattr(evidence, 'mask_path')}",
        f"- Overlay: {getattr(evidence, 'overlay_path')}",
        "",
        "## Key Regions",
    ]
    lines.extend(f"- {item}" for item in getattr(evidence, "key_regions"))
    lines.extend(["", "## Retrieved Knowledge"])
    lines.extend(f"- {item}" for item in report.retrieved_context)
    lines.extend(["", "## Recommendations"])
    lines.extend(f"- {item}" for item in report.recommendations)
    lines.append("")
    return "\n".join(lines)
