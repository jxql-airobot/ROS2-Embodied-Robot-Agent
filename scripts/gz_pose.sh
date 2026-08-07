#!/usr/bin/env bash
# Print the simple_diffbot world pose as: x y z qw qz
set +e
gz model -m simple_diffbot -i 2>/dev/null | awk '
  /^is_static: false/ { f=1 }
  f && /position/ { getline; x=$2; getline; y=$2; getline; z=$2 }
  f && /orientation/ { getline; qx=$2; getline; qy=$2; getline; qz=$2; getline; qw=$2; print x, y, z, qw, qz; exit }
'
