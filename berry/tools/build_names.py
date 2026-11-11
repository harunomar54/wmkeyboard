#!/usr/bin/env python3
"""Builds BB-Keyboard's name capitals and name dictionary.

Inputs (paths): AOSP en_US wordlist (.combined text), the SSA national baby
names folder (yobYYYY.txt files), WM's bundled English list (en.txt), the
bundled capitals (en_caps.txt), berry/names/arabic_names.txt and
berry/names/exclude.txt.

A name becomes a capital only when typing it in small letters can mean
nothing else:
  1. not on the exclude list (everyday words in Muslim English);
  2. AOSP's English list has no ordinary lower-case word for it, or only a
     rare one (f < 30), or writes it with a capital far more often (capital
     30+ above lower case, lower case under 75);
  3. it is not a likely slip for a common word (a QWERTY-neighbour swap,
     a transposition, one letter dropped or added), unless it is a name
     people actually carry: in the hand list, or 20,000+ US births;
  4. for an SSA-only name, at least MIN_BIRTHS US births since 1880.

Writes: <out>/caps_add.txt (new capitals), <out>/names-en-ar.combined (an
AOSP-format dictionary of every kept name, for completions), and
<out>/report.txt (counts and what was turned away and why).
"""
import math
import os
import re
import sys
from collections import defaultdict

aosp_path, ssa_dir, en_txt, caps_path, arabic_path, exclude_path, out = sys.argv[1:8]
MIN_BIRTHS = 300
POPULAR = 20000

# ---- inputs ----
freq = {}
entry = re.compile(r"^\s*word=([^,]+),f=(\d+)")
for line in open(aosp_path, encoding="utf-8"):
    m = entry.match(line)
    if m:
        freq[m.group(1)] = int(m.group(2))
common = {w: f for w, f in freq.items() if f >= 100 and w.isalpha() and w == w.lower()}

births = defaultdict(int)
for name in os.listdir(ssa_dir):
    if not re.match(r"yob\d{4}\.txt$", name):
        continue
    for line in open(os.path.join(ssa_dir, name), encoding="utf-8", errors="replace"):
        parts = line.strip().split(",")
        if len(parts) == 3:
            births[parts[0]] += int(parts[2])

existing = {l.strip() for l in open(caps_path, encoding="utf-8") if l.strip() and not l.startswith("#")}
existing_keys = {w.lower() for w in existing}
exclude = {l.strip().lower() for l in open(exclude_path, encoding="utf-8") if l.strip() and not l.startswith("#")}

# A rare spelling one slip from a very common name is a misspelling of it
# (jhon, micheal), not a name of its own.
for name, count in births.items():
    if count >= 200000:
        common.setdefault(name.lower(), 255)
for name in existing:
    if name[:1].isupper() and name.isalpha():
        common.setdefault(name.lower(), 255)

curated = []
for line in open(arabic_path, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    for name in (n.strip() for n in line.split(",")):
        if name and " " not in name:
            curated.append(name)
curated_keys = {n.lower() for n in curated}

# ---- typo neighbours ----
ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
pos = {c: (r, i) for r, row in enumerate(ROWS) for i, c in enumerate(row)}
def adjacent(a, b):
    if a not in pos or b not in pos:
        return False
    (r1, c1), (r2, c2) = pos[a], pos[b]
    # Rows are offset by half a key; neighbours are within one row and one column.
    return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1 and (a != b)

def slip_of(key):
    """A common word this spelling is one plausible slip away from, or None."""
    n = len(key)
    for i in range(n):  # neighbour swapped in
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c != key[i] and adjacent(c, key[i]):
                w = key[:i] + c + key[i + 1:]
                if w in common:
                    return w
    for i in range(n - 1):  # two letters crossed
        w = key[:i] + key[i + 1] + key[i] + key[i + 2:]
        if w != key and w in common:
            return w
    for i in range(n):  # a letter too many
        w = key[:i] + key[i + 1:]
        if len(w) >= 2 and w in common:
            return w
    for i in range(n + 1):  # a letter missed
        for c in "abcdefghijklmnopqrstuvwxyz":
            w = key[:i] + c + key[i:]
            if w in common:
                return w
    return None

def shaped(name):
    if name.startswith("Mc") and len(name) > 3 and name[2].islower():
        return "Mc" + name[2].upper() + name[3:]
    return name

# ---- decide ----
kept = {}
turned = defaultdict(list)
def consider(name, source):
    key = name.lower()
    if key in kept or key in existing_keys:
        return
    if not (2 <= len(key) <= 24) or not name[0].isupper() or not re.fullmatch(r"[^\W\d_]+(?:['-][^\W\d_]+)*", name):
        turned["shape"].append(name)
        return
    if key in exclude:
        turned["everyday word (hand list)"].append(name)
        return
    lf = freq.get(key)
    cf = freq.get(name[0].upper() + name[1:], freq.get(name, 0))
    if lf is not None and lf >= 30 and not (cf - lf >= 30 and lf < 75):
        turned["English word"].append(f"{name}({cf}/{lf})")
        return
    popular = key in curated_keys or births.get(name, 0) >= POPULAR
    if source == "ssa" and births.get(name, 0) < MIN_BIRTHS:
        turned["too rare"].append(name)
        return
    if source == "ssa" and len(key) < 3:
        turned["shape"].append(name)
        return
    if not popular and key.isascii():
        slip = slip_of(key)
        if slip:
            turned["slip for a common word"].append(f"{name}~{slip}")
            return
    kept[key] = shaped(name)

for name in curated:
    consider(name, "curated")
for name, count in sorted(births.items(), key=lambda kv: -kv[1]):
    consider(name, "ssa")

# Curated names that are one slip from a common word: kept, but listed so
# the trade-off can be read.
curated_slips = sorted(f"{kept[k]}~{s}" for k in curated_keys if k in kept and k.isascii() and (s := slip_of(k)))

os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "caps_add.txt"), "w", encoding="utf-8") as fh:
    for name in sorted(kept.values(), key=str.lower):
        fh.write(name + "\n")

def f_of(name):
    b = births.get(name, 0)
    if name.lower() in curated_keys:
        b = max(b, 30000)
    return max(60, min(200, int(40 + 14 * math.log10(max(b, 1)) * 3)))

with open(os.path.join(out, "names-en-ar.combined"), "w", encoding="utf-8") as fh:
    fh.write("dictionary=main:en_names,locale=en,description=Names (English and Arabic),date=1731300000,version=1\n")
    for name in sorted(kept.values(), key=lambda n: -f_of(n)):
        f = f_of(name)
        fh.write(f" word={name},f={f},flags=,originalFreq={f}\n")

with open(os.path.join(out, "report.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"kept {len(kept)} (curated {sum(1 for k in kept if k in curated_keys)})\n")
    for why, names in turned.items():
        fh.write(f"turned away, {why}: {len(names)}\n  " + " ".join(names[:400]) + "\n")
    fh.write(f"curated names one slip from a common word (kept): {len(curated_slips)}\n  " + " ".join(curated_slips) + "\n")
print(open(os.path.join(out, "report.txt"), encoding="utf-8").read()[:6000])
