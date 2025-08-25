#!/usr/bin/env python3
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('job')
args = parser.parse_args()
job = args.job

if job == 'job1':
    # Join Trips with Taxis
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2:  # Taxis.txt
            taxi_id, company_id = parts
            print(f"{taxi_id}\tC\t{company_id}")
        else:  # Trips.txt
            trip_id, taxi_id = parts[0], parts[1]
            print(f"{taxi_id}\tT\t{trip_id}")

elif job == 'job2':
    # Pass through company_id for counting
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        company_id, _ = line.split("\t")
        print(f"{company_id}\t1")

elif job == 'job3':
    # Option A: total first for sorting
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        company_id, total = line.split("\t")
        print(f"{total}\t{company_id}")

   