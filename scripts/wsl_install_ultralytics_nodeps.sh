#!/usr/bin/env bash
# Install ultralytics WITHOUT pulling torch/torchvision/CUDA from PyPI
# (torch 2.6.0+cpu is already installed). Falls back gracefully.
set +e
pkill -9 -f "pip3 install" 2>/dev/null
sleep 1

echo ">> installing ultralytics --no-deps"
pip3 install --user --no-deps ultralytics 2>&1 | tail -3

echo ">> installing small missing deps"
pip3 install --user --no-deps pillow seaborn ultralytics-thop 2>&1 | tail -3

echo ">> installing torchvision 0.21.0 (matches torch 2.6.0) --no-deps"
pip3 install --user --no-deps torchvision==0.21.0 2>&1 | tail -3

echo ">> verify"
python3 - <<'EOF'
try:
    import ultralytics
    print("ultralytics", ultralytics.__version__)
except Exception as exc:
    print("ultralytics FAIL:", type(exc).__name__, exc)
try:
    import torch
    import torchvision
    print("torch", torch.__version__, "torchvision", torchvision.__version__)
except Exception as exc:
    print("torchvision FAIL:", type(exc).__name__, exc)
EOF
