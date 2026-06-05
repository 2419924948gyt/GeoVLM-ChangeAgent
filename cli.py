from __future__ import annotations

import argparse
import json

from src.rs_vlm_agent import analyze_scene


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the remote-sensing VLM agent.")
    parser.add_argument("--pre", required=True, help="Path to the pre-event image.")
    parser.add_argument("--post", required=True, help="Path to the post-event image.")
    parser.add_argument(
        "--instruction",
        default="Analyze major land-cover changes.",
        help="Natural language interpretation request.",
    )
    parser.add_argument(
        "--model-mode",
        default="heuristic",
        choices=["heuristic", "api", "qwen_api", "dashscope"],
        help="Use heuristic local report or OpenAI-compatible VLM API report.",
    )
    parser.add_argument("--output-dir", default="outputs", help="Directory for outputs.")
    args = parser.parse_args()

    report = analyze_scene(
        args.pre,
        args.post,
        args.instruction,
        model_mode=args.model_mode,
        output_dir=args.output_dir,
    )
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
