#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate rscd
cd "$(dirname "$0")"

python scripts/create_demo_data.py
python cli.py \
  --pre demo_data/pre.png \
  --post demo_data/post.png \
  --instruction "请严格依据算法证据分析这组遥感影像中的建筑和道路变化，并给出结构化中文报告。不要把变化比例为0的区域描述为主要变化区。" \
  --model-mode qwen_api \
  --output-dir outputs/api_demo
