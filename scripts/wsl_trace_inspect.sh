#!/usr/bin/env bash
# Inspect the latest trace log: find the python pub step and surrounding lines.
set +e
F=$(ls -t /tmp/trace_*.log 2>/dev/null | head -1)
echo "file=$F"
LINE=$(grep -an "pub_robot_command.py" "$F" | tail -1 | cut -d: -f1)
echo "pub_line=$LINE"
if [ -n "$LINE" ]; then
  START=$((LINE - 5))
  sed -n "${START},$((LINE + 30))p" "$F"
fi
