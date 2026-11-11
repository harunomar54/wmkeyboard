#!/usr/bin/env python3
"""Lists words AOSP's English list spells mostly with a capital.

AOSP's en_US wordlist keeps "John" and "john" as separate entries with their
own frequencies (0-255, log scale). WM's bundled capitals (en_caps.txt) take
only words AOSP never writes in small letters, so a name that also has a rare
lower-case use (john, billy) never capitalizes. This prints, as TSV, every
key the bundled English list has where the capitalized entry outranks the
lower-case one, with both frequencies, so the cut can be reviewed by hand.

usage: name_capitals.py <en_US_wordlist.combined> <app/dictionaries-src/en.txt> <en_caps.txt>
"""
import re
import sys

combined, bundled_path, caps_path = sys.argv[1:4]
entry = re.compile(r"^\s*word=([^,]+),f=(\d+)")
freq = {}
with open(combined, encoding="utf-8") as fh:
    for line in fh:
        m = entry.match(line)
        if m:
            freq[m.group(1)] = int(m.group(2))
bundled = set()
with open(bundled_path, encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("#") or not line.strip():
            continue
        bundled.add(re.split(r"[\t ]", line.strip())[0])
with open(caps_path, encoding="utf-8") as fh:
    have = {l.strip() for l in fh if l.strip() and not l.startswith("#")}
rows = []
for word, f in freq.items():
    if not word[:1].isupper() or not word[1:].islower() or not word.isalpha():
        continue
    low = word.lower()
    if low not in bundled or word in have or low not in freq:
        continue
    rows.append((f - freq[low], word, f, freq[low]))
rows.sort(reverse=True)
print("margin\tword\tcap_f\tlower_f")
for margin, word, f, lf in rows:
    print(f"{margin}\t{word}\t{f}\t{lf}")
