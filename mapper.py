#!/usr/bin/env python3
import sys

def get_trip_type(fare):
    if fare >= 200.0:
        return "long"
    elif fare >= 100.0:
        return "medium"
    else:
        return "short"

for line in sys.stdin:
    parts = line.strip().split(',')
    # Trips.txt format: Trip#, Taxi#, fare, distance, pickup_x, pickup_y, dropoff_x, dropoff_y
    if len(parts) != 8:
        continue
    try:
        taxi_id = parts[1].strip()
        fare = float(parts[2].strip())
    except ValueError:
        continue

    trip_type = get_trip_type(fare)

    # For a single trip: count = 1, max = fare, min = fare, avg = fare
    print(f"{taxi_id}\t{trip_type}\t1\t{fare:.2f}\t{fare:.2f}\t{fare:.2f}")
