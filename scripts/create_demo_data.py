from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    out = Path("demo_data")
    out.mkdir(parents=True, exist_ok=True)

    pre = Image.new("RGB", (512, 512), "#5d8f61")
    draw = ImageDraw.Draw(pre)
    draw.rectangle((40, 50, 210, 230), fill="#6aa86d")
    draw.rectangle((260, 70, 450, 250), fill="#708a58")
    draw.line((30, 420, 480, 360), fill="#6e6e6e", width=22)
    draw.rectangle((80, 280, 140, 340), fill="#b6b0a0")

    post = pre.copy()
    draw_post = ImageDraw.Draw(post)
    draw_post.rectangle((300, 285, 410, 390), fill="#d8d0bd")
    draw_post.rectangle((150, 285, 230, 360), fill="#cfc7b6")
    draw_post.line((40, 150, 470, 145), fill="#747474", width=18)

    pre.save(out / "pre.png")
    post.save(out / "post.png")
    print(f"Wrote {out / 'pre.png'} and {out / 'post.png'}")


if __name__ == "__main__":
    main()

