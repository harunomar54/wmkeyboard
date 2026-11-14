import json, re
# Every word in the Quran and hadith lists built earlier, with diacritics
# stripped: a trigger must not be one of them, or typing that word would
# expand it.
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
def bare(w): return TASHKEEL.sub("", w)
words = set()
for f in ["/home/claude/arpack/out/quran-ar.combined", "/home/claude/arpack/out/hadith-ar.combined"]:
    for line in open(f, encoding="utf-8"):
        m = re.match(r"\s*word=([^,]+),", line)
        if m: words.add(bare(m.group(1)))
print("Arabic words checked against:", len(words))

# (Arabic triggers: the first letters people type, phrase). Triggers are the
# starts of the phrase's first word (or its usual run-together spelling),
# never a whole word.
P = [
(["السلا", "السلام ع", "اسلا"], "السلام عليكم ورحمة الله وبركاته"),
(["وعليكمال", "وعليكم الس", "وعليكما"], "وعليكم السلام ورحمة الله وبركاته"),
(["الحمدل", "الحمدلل", "الحم"], "الحمد لله"),
(["الحمدللهرب", "الحمدلر"], "الحمد لله رب العالمين"),
(["ماشا", "ماشاء", "ماش"], "ما شاء الله"),
(["انشا", "انشاء", "إنشا", "إنشاء"], "إن شاء الله"),
(["سبحانا", "سبحانال", "سبحانالل"], "سبحان الله"),
(["سبحانالله وب", "سبحاناللهوب"], "سبحان الله وبحمده"),
(["استغ", "استغف", "أستغ", "أستغف"], "أستغفر الله"),
(["الله اك", "اللهاك", "اللهأك"], "الله أكبر"),
(["لاالهال", "لا اله ال", "لااله"], "لا إله إلا الله"),
(["جزاكال", "جزاكالل", "جزا"], "جزاك الله خيرًا"),
(["جزاكمال", "جزاكم ال"], "جزاكم الله خيرًا"),
(["باركال", "بارك ال", "باركالل"], "بارك الله فيك"),
(["تباركال", "تبارك ال"], "تبارك الله"),
(["لاحول", "لاحو"], "لا حول ولا قوة إلا بالله"),
(["انالل", "إنالل", "انا لل"], "إنا لله وإنا إليه راجعون"),
(["حسبناال", "حسبنا ال", "حسبنال"], "حسبنا الله ونعم الوكيل"),
(["حسبيال", "حسبي ال", "حسبيالل"], "حسبي الله ونعم الوكيل"),
(["اعوذ", "أعوذب", "اعوذب"], "أعوذ بالله من الشيطان الرجيم"),
(["بسمال", "بسم ال", "بسمالل"], "بسم الله"),
(["بسماللهالر", "بسم الله الر"], "بسم الله الرحمن الرحيم"),
(["رحمهال", "رحمه ال"], "رحمه الله"),
(["رحمهاال", "رحمها ال"], "رحمها الله"),
(["رضيال", "رضي ال", "رضياللهعنه"], "رضي الله عنه"),
(["رضياللهعنها"], "رضي الله عنها"),
(["رضياللهعنهم"], "رضي الله عنهم"),
(["صلىال", "صلى ال", "صلاللهعل"], "صلى الله عليه وسلم"),
(["عليهالس", "عليه الس"], "عليه السلام"),
(["حياكال", "حياك ال", "حيكال"], "حياك الله"),
(["حياكمال", "حياكم ال"], "حياكم الله"),
(["فيامان", "في امان", "فيأمان"], "في أمان الله"),
(["يرحمكال", "يرحمك ال"], "يرحمك الله"),
(["اللهم ام", "اللهمام", "اللهمآ"], "اللهم آمين"),
(["عيدمب", "عيد مب"], "عيد مبارك"),
(["رمضانمب", "رمضان مب"], "رمضان مبارك"),
(["رمضانكر", "رمضان كر"], "رمضان كريم"),
(["جمعةمب", "جمعة مب", "جمعهمب"], "جمعة مباركة"),
(["تقبلال", "تقبل ال"], "تقبل الله منا ومنكم"),
(["واللهاع", "والله اع", "واللهأع"], "والله أعلم"),
(["اخيالك", "أخي الك", "اخي الك"], "أخي الكريم"),
(["اختيالك", "أختي الك", "اختي الك"], "أختي الكريمة"),
(["صباحال", "صباح ال"], "صباح الخير"),
(["مساءال", "مساء ال", "مساال"], "مساء الخير"),
(["معالس", "مع الس"], "مع السلامة"),
(["اهلاوس", "أهلا وس", "اهلا وس"], "أهلًا وسهلًا"),
]
snips, seen, sid = [], set(), 900
for trigs, ar in P:
    keep = []
    for t in trigs:
        b = bare(t)
        # A trigger of several words fires when its last word is typed after
        # the others; that last word, like a one-word trigger, must not be a
        # word in its own right.
        if bare(t.split()[-1]) in words:
            print("  skipped, a real word:", t, "->", ar)
            continue
        if b == bare(ar.split()[0]):
            print("  skipped, the whole first word:", t)
            continue
        assert b not in seen, ("trigger used twice", t)
        seen.add(b); keep.append(t)
    assert keep, ar
    sid += 1
    snips.append({"id": sid, "label": ar, "text": ar, "trigger": keep[0], "aliases": keep[1:]})
json.dump({"format": "wmkeyboard-snippets", "version": 2, "appVersion": 0, "appVersionName": "", "snippets": snips},
          open("arabic-autocomplete.wmsnippets.json", "w"), ensure_ascii=False, indent=2)
print(len(snips), "phrases")
for s in snips: print(f"{s['trigger']:<12} {' '.join(s['aliases']):<28} -> {s['text']}")
