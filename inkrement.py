#!/usr/bin/env python3
import sys
import re
from collections import defaultdict

start_val = None
count = 0
val_counter = defaultdict(int)

for line in sys.stdin:
    match = re.match(r'^(\d{4})', line)
    if match:
        num = match.group(1)
        if start_val is None:
            start_val = num
        count += 1
        prefix = num[:2]
        val_counter[prefix] += 1
        print(f"Zeile {count}: Start={start_val}, Aktuelle={num}, Gruppe={prefix}, Vorkommen={val_counter[prefix]}")

