from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass
class ChangeDetectionResult:
    changed_ratio: float
    confidence: str
    region_descriptions: list[str]
    mask_path: Path
    overlay_path: Path


def detect_changes(
    pre_image: str | Path,
    post_image: str | Path,
    output_dir: str | Path,
    threshold: int = 38,
) -> ChangeDetectionResult:
    """Compute a lightweight remote-sensing change mask.

    This baseline intentionally avoids heavy dependencies so the project can be
    demonstrated on a fresh machine. It can later be replaced by BIT, ChangeFormer,
    SAM-assisted masks, or a custom change-detection network.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pre = _load_rgb(pre_image)
    post = _load_rgb(post_image)
    post = post.resize(pre.size)

    pre_arr = np.asarray(pre).astype(np.int16)
    post_arr = np.asarray(post).astype(np.int16)
    diff = np.abs(post_arr - pre_arr).mean(axis=2).astype(np.uint8)
    mask = (diff > threshold).astype(np.uint8) * 255
    mask = _remove_salt_noise(mask)

    changed_ratio = float((mask > 0).mean())
    confidence = _confidence_from_ratio(changed_ratio)

    mask_img = Image.fromarray(mask, mode="L")
    overlay = _make_overlay(post, mask)

    mask_path = output_path / "change_mask.png"
    overlay_path = output_path / "change_overlay.png"
    mask_img.save(mask_path)
    overlay.save(overlay_path)

    return ChangeDetectionResult(
        changed_ratio=changed_ratio,
        confidence=confidence,
        region_descriptions=_describe_regions(mask),
        mask_path=mask_path,
        overlay_path=overlay_path,
    )


def _load_rgb(path: str | Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return image


def _remove_salt_noise(mask: np.ndarray) -> np.ndarray:
    padded = np.pad(mask > 0, 1, mode="constant")
    neighbors = np.zeros_like(mask, dtype=np.uint8)
    for dy in range(3):
        for dx in range(3):
            neighbors += padded[dy : dy + mask.shape[0], dx : dx + mask.shape[1]]
    return ((neighbors >= 4) * 255).astype(np.uint8)


def _make_overlay(image: Image.Image, mask: np.ndarray) -> Image.Image:
    arr = np.asarray(image).astype(np.float32)
    red = np.zeros_like(arr)
    red[..., 0] = 255
    alpha = (mask > 0)[..., None].astype(np.float32) * 0.45
    overlay = arr * (1.0 - alpha) + red * alpha
    return Image.fromarray(np.clip(overlay, 0, 255).astype(np.uint8), mode="RGB")


def _confidence_from_ratio(ratio: float) -> str:
    if ratio < 0.005:
        return "low_change_or_uncertain"
    if ratio < 0.08:
        return "moderate"
    return "high_change_detected"


def _describe_regions(mask: np.ndarray) -> list[str]:
    h, w = mask.shape
    regions = {
        "upper_left": mask[: h // 2, : w // 2],
        "upper_right": mask[: h // 2, w // 2 :],
        "lower_left": mask[h // 2 :, : w // 2],
        "lower_right": mask[h // 2 :, w // 2 :],
    }
    ranked = sorted(
        ((name, float((region > 0).mean())) for name, region in regions.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    return [f"{name}: changed_ratio={ratio:.2%}" for name, ratio in ranked]

