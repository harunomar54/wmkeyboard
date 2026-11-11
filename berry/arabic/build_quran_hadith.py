"""Builds AOSP `.combined` word lists with word pairs/triples for WM Keyboard's
Custom dictionaries (Arabic): the Quran (Tanzil simple text) and the matn of
Sahih al-Bukhari and Sahih Muslim (fawazahmed0/hadith-api, public-domain matn).

Vowel marks are stripped and hamza forms kept, which is how Arabic is typed."""
import json, math, re, sys
from collections import Counter

SRC, OUT = sys.argv[1], sys.argv[2]
HARAKAT = re.compile("[ؐ-ًؚ-ٰٟۖ-ۭـ]")
NOT_AR = re.compile("[^ء-غف-يٱ]+")
SALLA = "صلى الله عليه وسلم"

def clean(text):
    text = HARAKAT.sub("", text).replace("ٱ", "ا")
    return text

def tokens(text):
    return [t for t in NOT_AR.split(clean(text)) if t]

def matn(text):
    t = clean(text)
    i = t.find(SALLA)
    if i < 0:
        return None  # no prophetic statement marker: mostly chains and reports
    body = t[i + len(SALLA):]
    toks = tokens(body)
    while toks and toks[0] in ("قال", "يقول", "فقال", "انه", "أنه", "قالت"):
        toks = toks[1:]
    return toks if len(toks) >= 3 else None

def ngrams(seqs):
    uni, bi, tri = Counter(), Counter(), Counter()
    for s in seqs:
        uni.update(s)
        for i in range(1, len(s)):
            bi[(s[i-1], s[i])] += 1
            if i >= 2:
                tri[(s[i-2], s[i-1], s[i])] += 1
    return uni, bi, tri

def scale(count, top, lo, hi):
    return max(lo, min(hi, round(lo + (hi - lo) * math.log1p(count) / math.log1p(top))))

def write(path, name, desc, uni, bi, tri, word_hi, pair_lo):
    top_u = max(uni.values()); top_b = max(bi.values()); top_t = max(tri.values())
    by_first = {}
    for (a, b), c in bi.items():
        by_first.setdefault(a, []).append(("b", (b,), c))
    for (a, b, c3), c in tri.items():
        by_first.setdefault(b, []).append(("t", (a, c3), c))
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"dictionary=main:ar,locale=ar,description={desc},date=1731300000,version=1\n")
        for w, c in uni.most_common():
            f.write(f" word={w},f={scale(c, top_u, 40, word_hi)},flags=,originalFreq={c}\n")
            for kind, rest, c2 in by_first.get(w, ()):
                if kind == "b":
                    f.write(f"  bigram={rest[0]},f={scale(c2, top_b, pair_lo, 255)}\n")
        # triples: context is the two words before, [0] the nearest
        for (a, b, c3), c in tri.items():
            f.write(f" ngram={c3},f={scale(c, top_t, pair_lo, 255)}\n  prev_word[0]={b}\n  prev_word[1]={a}\n")
    import os
    print(f"{name}: {len(uni)} words, {len(bi)} pairs, {len(tri)} triples, {os.path.getsize(path)/1e6:.1f} MB")

quran = json.load(open(f"{SRC}/ara-quransimple.min.json"))["quran"]
surahs = {}
for v in quran:
    surahs.setdefault(v["chapter"], []).extend(tokens(v["text"]))  # ayahs flow into the next
q = ngrams(surahs.values())
write(f"{OUT}/quran-ar.combined", "Quran", "Quran (Tanzil simple text)", *q, word_hi=170, pair_lo=60)

had = []
for book in ("ara-bukhari.min.json", "ara-muslim.min.json"):
    d = json.load(open(f"{SRC}/{book}"))
    n = 0
    for h in d["hadiths"]:
        m = matn(h.get("text") or "")
        if m: had.append(m); n += 1
    print(book, "matns kept:", n, "of", len(d["hadiths"]))
h = ngrams(had)
write(f"{OUT}/hadith-ar.combined", "Hadith", "Sahih al-Bukhari and Sahih Muslim (matn)", *h, word_hi=150, pair_lo=40)
