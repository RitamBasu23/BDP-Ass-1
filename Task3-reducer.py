#!/usr/bin/env python3
import sys
from collections import defaultdict

if len(sys.argv) < 2:
    sys.exit(1)

job = sys.argv[1]

if job == 'job1':
    # Reducer for join
    taxi_to_company = {}
    trips = defaultdict(list)
    for line in sys.stdin:
        line = line.strip()
        key, tag, value = line.split("\t")
        if tag == 'C':
            taxi_to_company[key] = value
        elif tag == 'T':
            trips[key].append(value)
    for taxi_id in trips:
        company_id = taxi_to_company.get(taxi_id)
        if company_id:
            for _ in trips[taxi_id]:
                print(f"{company_id}\t1")

elif job == 'job2':
    # Reducer for counting trips per company
    counts = defaultdict(int)
    for line in sys.stdin:
        line = line.strip()
        company_id, count = line.split("\t")
        counts[company_id] += int(count)
    for company_id in counts:
        print(f"{company_id}\t{counts[company_id]}")

elif job == 'job3':
    # Reducer for final sorting (flip back)
    for line in sys.stdin:
        line = line.strip()
        total, company_id = line.split("\t")
        print(f"{company_id}\t{total}")
