#!/usr/bin/env python3
"""
mapper.py - Hadoop Streaming Mapper for Household Electricity Pattern Analysis
Extracts Hour from Time and emits (Hour, (Global_active_power, 1))
"""
import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        # Skip header or empty line
        if not line or line.startswith("Date"):
            continue
        parts = line.split(";")
        if len(parts) >= 3:
            time_str = parts[1]
            power_str = parts[2]
            # Handle missing values denoted by '?' or empty
            if power_str == "?" or not power_str:
                continue
            try:
                hour = time_str.split(":")[0]
                power = float(power_str)
                # Output key \t value
                # Key: Hour (00 to 23), Value: power,1
                print(f"{hour}\t{power:.4f},1")
            except (ValueError, IndexError):
                continue

if __name__ == "__main__":
    main()
