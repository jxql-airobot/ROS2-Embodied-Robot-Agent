#!/usr/bin/env bash
set +e
if pgrep -f "pip3 install --user ultralytics" >/dev/null; then
  echo "pip_running"
else
  echo "pip_finished"
fi
python3 - <<'EOF'
mods = ["ultralytics", "matplotlib", "pandas", "pillow", "scipy", "seaborn", "tqdm", "requests"]
for m in mods:
    try:
        mod = __import__(m)
        print(m, getattr(mod, "__version__", "?"))
    except Exception as exc:
        print(m, "MISSING", type(exc).__name__)
EOF
python3 -c "import torchvision; print('torchvision', torchvision.__version__)" 2>&1 | tail -1
