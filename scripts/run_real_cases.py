from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.rs_vlm_agent import analyze_scene


CASES = [
    ("case_001_sysu_cd_00071", "pre.png", "post.png"),
    ("case_002_dsifn_46", "pre.jpg", "post.jpg"),
    ("case_003_cdd_svcd_0272", "pre.jpg", "post.jpg"),
]


def main() -> None:
    root = Path("real_cases")
    for case_name, pre_name, post_name in CASES:
        case_dir = root / case_name
        output_dir = Path("outputs") / "real_cases" / case_name
        report = analyze_scene(
            case_dir / pre_name,
            case_dir / post_name,
            "请分析这组真实遥感前后时相图像中的变化区域，说明主要变化位置、不确定性和后续验证建议。",
            model_mode="heuristic",
            output_dir=output_dir,
        )
        print(
            f"{case_name}: changed_ratio={report.evidence.changed_ratio:.2%}, "
            f"confidence={report.evidence.confidence}, overlay={report.evidence.overlay_path}"
        )


if __name__ == "__main__":
    main()
