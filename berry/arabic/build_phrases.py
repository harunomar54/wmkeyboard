"""Everyday Islamic phrases as WM Keyboard custom dictionaries (AOSP .combined):
one Arabic, one in common English spellings. Each phrase is laid down as a word
sequence with strong pairs and triples, so it completes word by word."""
import sys
from collections import Counter
OUT = sys.argv[1]

AR = """
السلام عليكم
السلام عليكم ورحمة الله
السلام عليكم ورحمة الله وبركاته
وعليكم السلام
وعليكم السلام ورحمة الله
وعليكم السلام ورحمة الله وبركاته
بسم الله
بسم الله الرحمن الرحيم
الحمد لله
الحمد لله رب العالمين
الحمد لله على كل حال
إن شاء الله
إن شاء الله تعالى
ما شاء الله
ما شاء الله تبارك الله
تبارك الله
سبحان الله
سبحان الله وبحمده
سبحان الله وبحمده سبحان الله العظيم
سبحان الله والحمد لله ولا إله إلا الله والله أكبر
الله أكبر
لا إله إلا الله
لا إله إلا الله محمد رسول الله
أستغفر الله
أستغفر الله العظيم
أستغفر الله وأتوب إليه
لا حول ولا قوة إلا بالله
حسبنا الله ونعم الوكيل
حسبي الله ونعم الوكيل
إنا لله وإنا إليه راجعون
أعوذ بالله
أعوذ بالله من الشيطان الرجيم
توكلت على الله
الله المستعان
جزاك الله خيرا
جزاكم الله خيرا
وإياك
وإياكم
بارك الله فيك
بارك الله فيكم
وفيك بارك الله
وفيكم بارك الله
اللهم بارك
اللهم آمين
آمين
اللهم صل على محمد
اللهم صل وسلم على نبينا محمد
صلى الله عليه وسلم
عليه الصلاة والسلام
عليه السلام
رضي الله عنه
رضي الله عنها
رضي الله عنهم
رحمه الله
رحمها الله
رحمهم الله
الله يرحمه
الله يرحمها
حفظه الله
حفظك الله
الله يحفظك
يرحمك الله
يهديكم الله ويصلح بالكم
عز وجل
سبحانه وتعالى
تبارك وتعالى
في أمان الله
أحبك في الله
أحبك الله الذي أحببتني له
تقبل الله منا ومنكم
عيد مبارك
رمضان مبارك
رمضان كريم
جمعة مباركة
نسأل الله العافية
الله يعطيك العافية
شفاك الله
عظم الله أجركم
"""

EN = """
Assalamu alaikum
Assalamu alaikum wa rahmatullah
Assalamu alaikum wa rahmatullahi wa barakatuh
Assalamualaikum
Asalamualaikum
Salam
Salaam
Wa alaikum assalam
Wa alaikum assalam wa rahmatullahi wa barakatuh
Walaikum salam
Walaikumsalam
Alhamdulillah
Alhamdulillah rabbil alameen
InshaAllah
Inshallah
In sha Allah
MashaAllah
Mashallah
MashaAllah tabarakAllah
TabarakAllah
SubhanAllah
Subhanallah
SubhanAllahi wa bihamdihi
Astaghfirullah
Allahu Akbar
Allah
Ya Allah
Allahumma ameen
Ameen
Bismillah
Bismillahir rahmanir raheem
La ilaha illallah
La hawla wa la quwwata illa billah
Hasbunallahu wa ni'mal wakeel
Innalillahi wa inna ilayhi raji'un
A'udhu billah
JazakAllah khair
JazakAllahu khairan
Jazakallah
BarakAllahu feek
BarakAllahu feekum
Barakallah
Wa iyyak
Wa iyyakum
Rahimahullah
RadiAllahu anhu
RadiAllahu anha
Alayhis salam
Yarhamukallah
Fi amanillah
Ramadan Mubarak
Ramadan Kareem
Eid Mubarak
Jummah Mubarak
Jumu'ah Mubarak
Taqabbal Allahu minna wa minkum
Allah SWT
Prophet Muhammad
Akhi
Ukhti
Sheikh
Quran
Hadith
Sunnah
Salah
Dua
Dhikr
Masjid
Jannah
Deen
Ummah
Halal
Haram
Wudu
Fajr
Dhuhr
Asr
Maghrib
Isha
Taraweeh
Iftar
Suhoor
Zakat
Sadaqah
Hajj
Umrah
Insha'Allah
"""

def build(text, lang, desc, path, shortcuts=()):
    seqs = [l.split() for l in text.strip().splitlines() if l.strip()]
    uni, bi, tri = Counter(), Counter(), Counter()
    for s in seqs:
        uni.update(s)
        for i in range(1, len(s)):
            bi[(s[i-1], s[i])] += 1
            if i >= 2: tri[(s[i-2], s[i-1], s[i])] += 1
    sc = dict(shortcuts)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"dictionary=main:{lang},locale={lang},description={desc},date=1731300000,version=1\n")
        for w in uni:
            f.write(f" word={w},f=230,flags=,originalFreq={230}\n")
            if w in sc: f.write(f"  shortcut={sc[w]},f=14\n")
            for (a, b), c in bi.items():
                if a == w: f.write(f"  bigram={b},f={min(255, 175 + 25 * c)}\n")
        for (a, b, c3), c in tri.items():
            f.write(f" ngram={c3},f={min(255, 195 + 20 * c)}\n  prev_word[0]={b}\n  prev_word[1]={a}\n")
    print(path, len(uni), "words", len(bi), "pairs", len(tri), "triples")

build(AR, "ar", "Everyday Islamic phrases (Arabic)", f"{OUT}/islamic-phrases-ar.combined")
EN_SHORT = "pbuh"
build(EN + "\n" + EN_SHORT, "en", "Everyday Islamic phrases (English spellings)",
      f"{OUT}/islamic-phrases-en.combined", shortcuts=[("pbuh", "ﷺ")])
