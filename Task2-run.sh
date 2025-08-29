#!/usr/bin/env bash
set -euo pipefail

# === Config (keep jar and file names exactly as required) ===
JAR="./hadoop-streaming-3.1.4.jar"
INPUT="/Input/Trips.txt"
FINAL_OUT="/Output/Task2"

# Find a Python on this node; use absolute path for containers too
PY="$(command -v python3 || true)"
if [[ -z "${PY}" ]]; then
  PY="$(command -v python || true)"
fi
if [[ -z "${PY}" ]]; then
  echo "No python interpreter found. Install python3 on all nodes." >&2
  exit 127
fi

# --- Windows line-ending guard (safe no-op on Linux) ---
sed -i 's/\r$//' Task2-run.sh mapper2.py reducer2.py reader.py || true

# 1) Build initial medoids_current.txt and get v
v="$($PY reader.py)"
if ! [[ -s medoids_current.txt ]]; then
  echo "medoids_current.txt missing after reader.py" >&2
  exit 1
fi

# 2) Clean final output
hadoop fs -rm -r -f "$FINAL_OUT" >/dev/null 2>&1 || true

# Keep previous medoids to detect convergence
cp medoids_current.txt medoids_prev.txt

iter=1
while (( iter <= v )); do
  ITER_OUT="/tmp/Task2_iter_${iter}"
  hadoop fs -rm -r -f "$ITER_OUT" >/dev/null 2>&1 || true

  # 3) Streaming round: 3 reducers, ship mapper/reducer + side file
  hadoop jar "$JAR" \
    -D mapreduce.job.name="Task2_PAM_iter_${iter}" \
    -D mapreduce.job.reduces=3 \
    -files mapper2.py,reducer2.py,medoids_current.txt \
    -input "$INPUT" \
    -output "$ITER_OUT" \
    -mapper  "$PY mapper2.py" \
    -reducer "$PY reducer2.py"

  # 4) Collect new medoids: reducer outputs lines "idx \t x \t y"
  hadoop fs -cat "${ITER_OUT}/part-*" > medoids_next_raw.txt || true
  if ! [[ -s medoids_next_raw.txt ]]; then
    echo "Empty reducer output; check mapper/reducer logs." >&2
    exit 127
  fi
  sort -n -k1,1 medoids_next_raw.txt > medoids_sorted.txt
  awk '{print $2 "\t" $3}' medoids_sorted.txt > medoids_current.txt

  # 5) Print iteration log: iteration number + list of medoids
  echo -n "Iteration ${iter}: "
  paste -sd'|' medoids_current.txt | sed 's/|/  |  /g'

  # 6) Convergence check
  if cmp -s medoids_current.txt medoids_prev.txt; then
    break
  fi
  cp medoids_current.txt medoids_prev.txt
  ((iter++))
done

# 7) Final output exactly k lines "x \t y" in /Output/Task2/part-00000
awk '{print $1 "\t" $2}' medoids_current.txt > Task2_output_parts.txt
hadoop fs -mkdir -p "$FINAL_OUT"
hadoop fs -put -f Task2_output_parts.txt "${FINAL_OUT}/part-00000"

echo "Done. Final medoids at ${FINAL_OUT}. Merge with:"
echo "  hadoop fs -getmerge /Output/Task2/part* Task2_output.txt"
