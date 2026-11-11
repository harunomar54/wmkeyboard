#!/usr/bin/env python3
"""Totals CRAN babynames' per-year counts into one name,sex,count file."""
import sys

import pyreadr

df = pyreadr.read_r(sys.argv[1])["babynames"]
totals = df.groupby(["name", "sex"])["n"].sum()
with open(sys.argv[2], "w", encoding="utf-8") as fh:
    for (name, sex), n in totals.items():
        fh.write(f"{name},{sex},{int(n)}\n")
print(len(totals), "name and sex pairs")
