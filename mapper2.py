#!/usr/bin/env python3
import sys, re, math, csv

# ---- Load current medoids from side file ----
medoids = []
try:
    with open("medoids_current.txt", "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            parts = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", ln)
            if len(parts) >= 2:
                x, y = float(parts[-2]), float(parts[-1])
                medoids.append((x, y))
except FileNotFoundError:
    print("ERROR: medoids_current.txt not found", file=sys.stderr)
    sys.exit(1)

if not medoids:
    print("ERROR: no medoids loaded", file=sys.stderr)
    sys.exit(1)

# ---- Read Trips.txt as CSV; use 3rd & 4th fields as drop-off (x,y) ----
reader = csv.reader(sys.stdin)
for row in reader:
    if not row:
        continue
    # some rows may have spaces; strip them
    row = [c.strip() for c in row if c is not None and c.strip() != ""]
    if len(row) < 4:
        # not enough columns; skip
        continue

    try:
        # Drop-off coordinates
        x = float(row[2])
        y = float(row[3])
    except Exception:
        # If parsing fails (e.g., weird row), try last-2-numbers fallback
        nums = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", ",".join(row))
        if len(nums) < 2:
            continue
        x = float(nums[-2]); y = float(nums[-1])

    # Nearest medoid (Euclidean)
    best_i, best_d2 = 0, None
    for i, (mx, my) in enumerate(medoids):
        dx, dy = x - mx, y - my
        d2 = dx*dx + dy*dy
        if best_d2 is None or d2 < best_d2:
            best_d2, best_i = d2, i

    # Key: medoid index; Value: x y
    print(f"{best_i}\t{x}\t{y}")
