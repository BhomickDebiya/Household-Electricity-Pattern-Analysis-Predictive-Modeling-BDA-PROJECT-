#!/usr/bin/env python3
"""
reducer.py - Hadoop Streaming Reducer for Household Electricity Pattern Analysis
Aggregates hourly sum of Global_active_power and total count to compute average active power (kW)
"""
import sys

def main():
    current_hour = None
    sum_power = 0.0
    count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            parts = line.split("\t")
            if len(parts) != 2:
                continue
            hour, val = parts
            power_str, cnt_str = val.split(",")
            power = float(power_str)
            cnt = int(cnt_str)
        except ValueError:
            continue

        if current_hour == hour:
            sum_power += power
            count += cnt
        else:
            if current_hour is not None:
                avg_power = sum_power / count if count > 0 else 0.0
                print(f"{current_hour}\t{avg_power:.4f}\t{count}")
            current_hour = hour
            sum_power = power
            count = cnt

    # Flush last key
    if current_hour is not None:
        avg_power = sum_power / count if count > 0 else 0.0
        print(f"{current_hour}\t{avg_power:.4f}\t{count}")

if __name__ == "__main__":
    main()
