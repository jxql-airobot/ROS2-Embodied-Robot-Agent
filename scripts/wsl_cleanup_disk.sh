#!/usr/bin/env bash
# Remove disk junk left by the failed torch/CUDA pip installs.
set +e

echo "== before =="
du -sh ~/.cache/pip /tmp ~/.local 2>/dev/null

echo ">> purging pip cache ..."
pip3 cache purge 2>&1 | tail -1

echo ">> removing pip temp dirs in /tmp ..."
rm -rf /tmp/pip-* 2>/dev/null
ls -d /tmp/pip-* 2>/dev/null || echo "no pip temp dirs left"

echo ">> checking ~/.local for broken torch/torchvision ..."
du -sh ~/.local/lib/python3.10/site-packages/* 2>/dev/null | sort -h | tail -8
if [ -d ~/.local/lib/python3.10/site-packages/torch ] && ! python3 -c "import torch; print('system torch', torch.__version__)" 2>/dev/null; then
  echo ">> removing broken ~/.local torch ..."
  rm -rf ~/.local/lib/python3.10/site-packages/torch
  rm -rf ~/.local/lib/python3.10/site-packages/torch-*.dist-info 2>/dev/null
fi

echo "== after =="
du -sh ~/.cache/pip /tmp ~/.local 2>/dev/null
