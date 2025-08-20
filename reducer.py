#!/usr/bin/env python3
import sys

current_key = None
total_count = 0
total_fare = 0.0
max_fare = float('-inf')
min_fare = float('inf')

def emit_result(key, count, max_f, min_f, avg_f):
    taxi_id, trip_type = key
    print(f"{taxi_id}\t{trip_type}\t{count}\t{max_f:.2f}\t{min_f:.2f}\t{avg_f:.2f}")

for line in sys.stdin:
    try:
        taxi_id, trip_type, count_str, max_str, min_str, avg_str = line.strip().split('\t')
        count = int(count_str)
        max_f = float(max_str)
        min_f = float(min_str)
        avg_f = float(avg_str)
        total_segment_fare = avg_f * count
    except ValueError:
        continue

    key = (taxi_id, trip_type)

    if current_key == key:
        # accumulate
        total_count += count
        total_fare += total_segment_fare
        max_fare = max(max_fare, max_f)
        min_fare = min(min_fare, min_f)
    else:
        # flush previous key
        if current_key is not None:
            avg = total_fare / total_count if total_count > 0 else 0
            emit_result(current_key, total_count, max_fare, min_fare, avg)

        # reset for new key
        current_key = key
        total_count = count
        total_fare = total_segment_fare
        max_fare = max_f
        min_fare = min_f

# flush last key
if current_key is not None:
    avg = total_fare / total_count if total_count > 0 else 0
    emit_result(current_key, total_count, max_fare, min_fare, avg)
