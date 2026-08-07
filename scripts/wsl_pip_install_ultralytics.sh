#!/usr/bin/env bash
# Install ultralytics with visible progress and a per-download timeout.
set +e
pkill -f "pip3 install --user ultralytics" 2>/dev/null
sleep 1
echo ">> pip3 install --user ultralytics (log: /tmp/pip_ultralytics.log)"
pip3 install --user ultralytics --no-cache-dir --timeout 30 \
  > /tmp/pip_ultralytics.log 2>&1 &
PID=$!
for _ in $(seq 1 60); do
  if ! kill -0 "$PID" 2>/dev/null; then
    break
  fi
  sleep 5
done
if kill -0 "$PID" 2>/dev/null; then
  echo "STILL_RUNNING after 300s"
  kill -9 "$PID" 2>/dev/null
fi
tail -15 /tmp/pip_ultralytics.log
python3 -c "import ultralytics; print('ultralytics', ultralytics.__version__)" 2>&1 | tail -1
