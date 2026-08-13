#!/usr/bin/env bash
# Idempotent, zero-traffic patch for ultralytics on CPU-only torch.
#
# torch 2.6.0+cpu and torchvision 0.21.0 (PyPI) are ABI-incompatible
# ("operator torchvision::nms does not exist"). ultralytics' AutoBackend.warmup()
# imports torchvision unconditionally, which crashes predict(). Detection does
# not actually need torchvision; this patch skips the broken import so NMS falls
# back to ultralytics' pure-Torch TorchNMS.nms.
#
# Re-run this after `pip3 install --upgrade ultralytics` (the patch lives in
# site-packages, not in this repo).
set -euo pipefail

PY="$(python3 - <<'PY'
import os
import ultralytics
print(os.path.join(os.path.dirname(ultralytics.__file__), "nn", "autobackend.py"))
PY
)"

if [ -z "$PY" ] || [ ! -f "$PY" ]; then
  echo "ERROR: could not locate ultralytics autobackend.py (is ultralytics installed?)" >&2
  exit 1
fi

MARK="except Exception:  # torch/torchvision ABI mismatch (CPU-only torch)"
if grep -qF "$MARK" "$PY"; then
  echo "already patched: $PY"
  exit 0
fi

[ -f "$PY.bak" ] || cp "$PY" "$PY.bak"
echo "backup: $PY.bak"

python3 - "$PY" <<'PY'
import sys

p = sys.argv[1]
with open(p, encoding="utf-8") as f:
    text = f.read()
text = text.replace("\r\n", "\n").replace("\r", "\n")
lines = text.split("\n")

idx = None
for i, line in enumerate(lines):
    if "import torchvision" in line and "noqa" in line and i > 0 and "if not self.end2end:" in lines[i - 1]:
        idx = i
        break
if idx is None:
    sys.exit("ERROR: target `import torchvision` line not found; ultralytics version may differ")

indent = lines[idx][: len(lines[idx]) - len(lines[idx].lstrip())]
block = [
    indent + "try:",
    indent + "    import torchvision  # noqa (import here triggers torchvision NMS use in nms.py)",
    indent + "except Exception:  # torch/torchvision ABI mismatch (CPU-only torch): fall back to pure-Torch NMS",
    indent + "    pass",
]
lines[idx : idx + 1] = block
with open(p, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("patched:", p)
PY
