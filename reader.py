#!/usr/bin/env python3
"""
reader.py
- Reads initialization.txt in the current directory.
- First non-empty numeric token = v (max iterations).
- Remaining numeric tokens are 2*k medoid coords: x1, y1, x2, y2, ...
- Writes medoids_current.txt (k lines: x<TAB>y).
- Prints v to STDOUT (no extra text).
"""
import re, sys

INIT_FILE = "initialization.txt"
OUT_FILE = "medoids_current.txt"
num_re = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

def die(msg, code=1):
    print(msg, file=sys.stderr); sys.exit(code)

def main():
    try:
        with open(INIT_FILE, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        die("ERROR: initialization.txt not found.")

    if not lines:
        die("ERROR: initialization.txt is empty.")

    first_nums = num_re.findall(lines[0])
    if not first_nums:
        die("ERROR: first line must contain v (integer/float).")
    try:
        v = int(float(first_nums[0]))
    except:
        die("ERROR: v must be an integer (or convertible).")

    floats = []
    for ln in lines[1:]:
        for t in num_re.findall(ln):
            floats.append(float(t))

    if len(floats) == 0:
        die("ERROR: no medoid coordinates found after v.")
    if len(floats) % 2 != 0:
        die("ERROR: odd number of medoid values; need (x,y) pairs.")

    try:
        with open(OUT_FILE, "w", encoding="utf-8") as out:
            for i in range(0, len(floats), 2):
                out.write(f"{floats[i]}\t{floats[i+1]}\n")
    except Exception as e:
        die(f"ERROR: cannot write medoids_current.txt: {e}")

    print(v)

if __name__ == "__main__":
    main()
