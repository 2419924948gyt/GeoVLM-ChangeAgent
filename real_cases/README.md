# Real Remote-Sensing Cases

This folder contains three real image pairs selected from local change-detection
datasets for project demonstration.

## Cases

| Case | Source dataset | Original split | Original id | Files |
| --- | --- | --- | --- | --- |
| `case_001_sysu_cd_00071` | SYSU-CD | test | `00071.png` | `pre.png`, `post.png`, `label.png` |
| `case_002_dsifn_46` | DSIFN-Dataset | test | `46.jpg` | `pre.jpg`, `post.jpg`, `label.tif` |
| `case_003_cdd_svcd_0272` | CDD/SVCD without_shift | test | `0272.jpg` | `pre.jpg`, `post.jpg`, `label.jpg` |

## Usage

Run one case:

```bash
python cli.py --pre real_cases/case_001_sysu_cd_00071/pre.png --post real_cases/case_001_sysu_cd_00071/post.png --instruction "请分析这组真实遥感前后时相图像中的变化区域" --model-mode heuristic --output-dir outputs/real_cases/case_001_sysu_cd_00071
```

These cases are meant for demonstration and qualitative inspection. The current
baseline is pixel-difference based, so real-case results may include seasonal,
illumination, registration, or sensor-related false positives.

