#!/usr/bin/env python3
import sys, math

def euclid(a,b):
    dx=a[0]-b[0]; dy=a[1]-b[1]
    return (dx*dx+dy*dy) ** 0.5

current_k = None
points = []

def flush():
    if not points: 
        return
    n = len(points)
    best_idx = 0
    best_cost = float("inf")
    for i in range(n):
        s=0.0; pi=points[i]
        for j in range(n):
            if i==j: continue
            s += euclid(pi, points[j])
        if s < best_cost:
            best_cost = s; best_idx=i
    m=points[best_idx]
    print(f"{current_k}\t{m[0]}\t{m[1]}")

for line in sys.stdin:
    line=line.strip()
    if not line: continue
    k, xy = line.split("\t",1)
    if current_k is not None and k != current_k:
        flush(); points=[]
    current_k=k
    x_str,y_str = xy.split(",",1)
    points.append((float(x_str), float(y_str)))

if current_k is not None:
    flush()
