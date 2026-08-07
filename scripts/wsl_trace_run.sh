#!/usr/bin/env bash
# Run another script under bash -x with a hard timeout, then show the tail.
set +e
SCRIPT="$1"
OUT="/tmp/trace_$$.log"
timeout -k 5 60 bash -x "$SCRIPT" > "$OUT" 2>&1
CODE=$?
echo "trace_exit=$CODE"
tail -50 "$OUT"
