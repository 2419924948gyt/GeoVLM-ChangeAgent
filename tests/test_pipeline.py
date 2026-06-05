from pathlib import Path
import unittest

from PIL import Image

from src.rs_vlm_agent import analyze_scene


class RemoteSensingAgentTest(unittest.TestCase):
    def test_analyze_scene_generates_report(self):
        root = Path("outputs/test")
        root.mkdir(parents=True, exist_ok=True)
        pre = root / "pre.png"
        post = root / "post.png"
        Image.new("RGB", (64, 64), "green").save(pre)
        changed = Image.new("RGB", (64, 64), "green")
        for x in range(20, 40):
            for y in range(20, 40):
                changed.putpixel((x, y), (220, 220, 220))
        changed.save(post)

        report = analyze_scene(pre, post, "分析建筑变化", output_dir=root)
        self.assertGreater(report.evidence.changed_ratio, 0)
        self.assertTrue(Path(report.evidence.overlay_path).exists())


if __name__ == "__main__":
    unittest.main()

