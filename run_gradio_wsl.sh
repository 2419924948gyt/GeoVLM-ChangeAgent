#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate rscd
cd "$(dirname "$0")"

export GRADIO_ANALYTICS_ENABLED=False
python scripts/create_demo_data.py
python app.py
