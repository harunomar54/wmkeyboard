import json, re
# The 114 surahs: number, Arabic name, English name, from quran.ai's
# Quran metadata (fetch_quran_metadata, manzils 1-7). Six Arabic names come
# there in the mushaf's own spelling and are given here as they are written
# in ordinary text (ابراهيم -> إبراهيم, سبإ -> سبأ, النبإ -> النبأ,
# الانسان -> الإنسان, الإنفطار -> الانفطار, الإنشقاق -> الانشقاق), and three
# English names in their common spelling (Al-Anbya, Ash-Shuraa, Ad-Duhaa).
S = [
(1,"الفاتحة","Al-Fatihah"),(2,"البقرة","Al-Baqarah"),(3,"آل عمران","Ali 'Imran"),(4,"النساء","An-Nisa"),
(5,"المائدة","Al-Ma'idah"),(6,"الأنعام","Al-An'am"),(7,"الأعراف","Al-A'raf"),(8,"الأنفال","Al-Anfal"),
(9,"التوبة","At-Tawbah"),(10,"يونس","Yunus"),(11,"هود","Hud"),(12,"يوسف","Yusuf"),(13,"الرعد","Ar-Ra'd"),
(14,"إبراهيم","Ibrahim"),(15,"الحجر","Al-Hijr"),(16,"النحل","An-Nahl"),(17,"الإسراء","Al-Isra"),
(18,"الكهف","Al-Kahf"),(19,"مريم","Maryam"),(20,"طه","Taha"),(21,"الأنبياء","Al-Anbiya"),(22,"الحج","Al-Hajj"),
(23,"المؤمنون","Al-Mu'minun"),(24,"النور","An-Nur"),(25,"الفرقان","Al-Furqan"),(26,"الشعراء","Ash-Shu'ara"),
(27,"النمل","An-Naml"),(28,"القصص","Al-Qasas"),(29,"العنكبوت","Al-'Ankabut"),(30,"الروم","Ar-Rum"),
(31,"لقمان","Luqman"),(32,"السجدة","As-Sajdah"),(33,"الأحزاب","Al-Ahzab"),(34,"سبأ","Saba"),(35,"فاطر","Fatir"),
(36,"يس","Ya-Sin"),(37,"الصافات","As-Saffat"),(38,"ص","Sad"),(39,"الزمر","Az-Zumar"),(40,"غافر","Ghafir"),
(41,"فصلت","Fussilat"),(42,"الشورى","Ash-Shura"),(43,"الزخرف","Az-Zukhruf"),(44,"الدخان","Ad-Dukhan"),
(45,"الجاثية","Al-Jathiyah"),(46,"الأحقاف","Al-Ahqaf"),(47,"محمد","Muhammad"),(48,"الفتح","Al-Fath"),
(49,"الحجرات","Al-Hujurat"),(50,"ق","Qaf"),(51,"الذاريات","Adh-Dhariyat"),(52,"الطور","At-Tur"),
(53,"النجم","An-Najm"),(54,"القمر","Al-Qamar"),(55,"الرحمن","Ar-Rahman"),(56,"الواقعة","Al-Waqi'ah"),
(57,"الحديد","Al-Hadid"),(58,"المجادلة","Al-Mujadila"),(59,"الحشر","Al-Hashr"),(60,"الممتحنة","Al-Mumtahanah"),
(61,"الصف","As-Saf"),(62,"الجمعة","Al-Jumu'ah"),(63,"المنافقون","Al-Munafiqun"),(64,"التغابن","At-Taghabun"),
(65,"الطلاق","At-Talaq"),(66,"التحريم","At-Tahrim"),(67,"الملك","Al-Mulk"),(68,"القلم","Al-Qalam"),
(69,"الحاقة","Al-Haqqah"),(70,"المعارج","Al-Ma'arij"),(71,"نوح","Nuh"),(72,"الجن","Al-Jinn"),
(73,"المزمل","Al-Muzzammil"),(74,"المدثر","Al-Muddaththir"),(75,"القيامة","Al-Qiyamah"),(76,"الإنسان","Al-Insan"),
(77,"المرسلات","Al-Mursalat"),(78,"النبأ","An-Naba"),(79,"النازعات","An-Nazi'at"),(80,"عبس","'Abasa"),
(81,"التكوير","At-Takwir"),(82,"الانفطار","Al-Infitar"),(83,"المطففين","Al-Mutaffifin"),(84,"الانشقاق","Al-Inshiqaq"),
(85,"البروج","Al-Buruj"),(86,"الطارق","At-Tariq"),(87,"الأعلى","Al-A'la"),(88,"الغاشية","Al-Ghashiyah"),
(89,"الفجر","Al-Fajr"),(90,"البلد","Al-Balad"),(91,"الشمس","Ash-Shams"),(92,"الليل","Al-Layl"),
(93,"الضحى","Ad-Duha"),(94,"الشرح","Ash-Sharh"),(95,"التين","At-Tin"),(96,"العلق","Al-'Alaq"),
(97,"القدر","Al-Qadr"),(98,"البينة","Al-Bayyinah"),(99,"الزلزلة","Az-Zalzalah"),(100,"العاديات","Al-'Adiyat"),
(101,"القارعة","Al-Qari'ah"),(102,"التكاثر","At-Takathur"),(103,"العصر","Al-'Asr"),(104,"الهمزة","Al-Humazah"),
(105,"الفيل","Al-Fil"),(106,"قريش","Quraysh"),(107,"الماعون","Al-Ma'un"),(108,"الكوثر","Al-Kawthar"),
(109,"الكافرون","Al-Kafirun"),(110,"النصر","An-Nasr"),(111,"المسد","Al-Masad"),(112,"الإخلاص","Al-Ikhlas"),
(113,"الفلق","Al-Falaq"),(114,"الناس","An-Nas"),
]
assert len(S) == 114 and [n for n, _, _ in S] == list(range(1, 115))
# Other spellings people type, by key.
EXTRA = {"yasin": ["yaseen"], "fatihah": ["fatiha"], "baqarah": ["baqara"], "imran": ["aliimran", "alimran"],
         "maidah": ["maida"], "tawbah": ["tawba", "taubah"], "rahman": ["rahmaan"], "kahf": [], "mulk": [],
         "ikhlas": ["ikhlaas"], "kawthar": ["kauthar", "kawsar"], "waqiah": ["waqia"], "jumuah": ["jumua", "jumah"],
         "muzzammil": ["muzammil"], "muddaththir": ["muddathir", "mudathir"], "taha": ["thaha"], "nas": ["naas"]}
def key(en):
    k = re.sub(r"^(Al|An|Ar|As|At|Ash|Ad|Adh|Az)-", "", en)
    k = {"Ali 'Imran": "imran", "Ya-Sin": "yasin"}.get(en, k)
    k = re.sub(r"[^a-z]", "", k.lower())
    # Spellings whose trigger would be a word you type: shud ("should"),
    # serum, sala.
    return {"hud": "hood", "rum": "room", "ala": "aala"}.get(k, k)
import sys
sys.path.insert(0, "/home/claude/arpack/arsnip")
TASHKEEL = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")
def bare(w): return TASHKEEL.sub("", w)
arwords = set()
for f in ["/home/claude/arpack/out/quran-ar.combined", "/home/claude/arpack/out/hadith-ar.combined"]:
    for line in open(f, encoding="utf-8"):
        m = re.match(r"\s*word=([^,]+),", line)
        if m: arwords.add(bare(m.group(1)))
def article(en):
    m = re.match(r"^(Al|An|Ar|As|At|Ash|Ad|Adh|Az)-", en)
    return m.group(1).lower() if m else None
used_ar = set()
def arabic_prefixes(ar):
    """'سورة ' + the start of a one-word name, a letter or two short of the
    whole name, never a real word: what you type before the name is done."""
    if " " in ar or len(ar) < 4: return []
    out = []
    for cut in (1, 2):
        p = ar[:-cut]
        if len(bare(p)) < 3 or bare(p) in arwords or p in used_ar: continue
        used_ar.add(p); out.append("سورة " + p)
    return out
snips, sid, seen = [], 1, set()
for n, ar, en in S:
    k = key(en)
    assert k not in seen, k
    seen.add(k)
    alts = EXTRA.get(k, [])
    snips.append({"id": sid, "label": f"{n}. {en} (Arabic)", "text": f"سورة {ar}", "trigger": "s" + k,
                  "aliases": ["s" + a for a in alts] + [f"s{n}"] + arabic_prefixes(ar)})
    sid += 1
    # The English spelling, from the way it is typed after "surah":
    # surah tahrim, surah at tahrim, surah al tahrim, surat tahrim, sura tahrim.
    # The long vowels people write doubled: tahreem, hadeed, noor, kafiroon.
    def longs(w):
        out = []
        i = w.rfind("i")
        if i > 0 and i >= len(w) - 3: out.append(w[:i] + "ee" + w[i+1:])
        u = w.rfind("u")
        if u > 0 and u >= len(w) - 3: out.append(w[:u] + "oo" + w[u+1:])
        return out
    names = list(dict.fromkeys([k] + alts + [v for nm in [k] + alts for v in longs(nm)]))
    arts = ["al"] + ([article(en)] if article(en) and article(en) != "al" else [])
    eng = []
    for word in ("surah", "surat", "sura"):
        for nm in names:
            eng.append(f"{word} {nm}")
            eng += [f"{word} {a} {nm}" for a in arts]
    eng = list(dict.fromkeys(eng))
    snips.append({"id": sid, "label": f"{n}. {en} (English)", "text": f"Surah {en}", "trigger": eng[0],
                  "aliases": eng[1:] + ["se" + nm for nm in [k] + alts]})
    sid += 1
pack = {"format": "wmkeyboard-snippets", "version": 2, "appVersion": 0, "appVersionName": "", "snippets": snips}
json.dump(pack, open("quran-surahs.wmsnippets.json", "w"), ensure_ascii=False, indent=2)

# Phrases: (trigger, [other spellings], Arabic). Fully written, hamza and
# tanween as in careful modern print. Triggers already used by the BB
# shortcuts (alh, assal, jazak, subhan, tabarka, azza, bissm, sallahu) are
# left to them.
P = [
("salam", ["salaam", "assalamualaikum", "asalamualaikum", "assalamualaykum", "salamualaikum"], "السلام عليكم"),
("salamfull", ["assalamualaikumwarahmatullahiwabarakatuh", "slmwrwb", "aswrwb"], "السلام عليكم ورحمة الله وبركاته"),
("walaikumsalam", ["waalaikumsalam", "wassalam", "walaikumassalam", "wslm"], "وعليكم السلام"),
("walaikumsalamfull", ["wswrwb"], "وعليكم السلام ورحمة الله وبركاته"),
("bismillah", ["bismilah"], "بسم الله"),
("bismillahfull", ["bismillahirrahmanirrahim"], "بسم الله الرحمن الرحيم"),
("alhamdulillah", ["alhamdulilah", "alhamdullilah", "hamdulillah", "alhamdolillah"], "الحمد لله"),
("alhamdulillahrab", ["alhamdulillahirabbilalamin"], "الحمد لله رب العالمين"),
("alhamdulillahkul", ["alhamdulillahalakullihal"], "الحمد لله على كل حال"),
("mashallah", ["mashaallah", "mashaalah", "mashalla"], "ما شاء الله"),
("inshallah", ["inshaallah", "inshalla"], "إن شاء الله"),
("subhanallah", ["subhanalah", "subhaanallah"], "سبحان الله"),
("subhanallahwabihamdihi", ["swb"], "سبحان الله وبحمده"),
("subhanallahazim", ["subhanallahilazim"], "سبحان الله العظيم"),
("allahuakbar", ["allahuakber"], "الله أكبر"),
("lailahaillallah", ["lailaha", "lailahaillalah"], "لا إله إلا الله"),
("astaghfirullah", ["astagfirullah", "astaghfirulah", "astaghfirallah"], "أستغفر الله"),
("astaghfirullahazim", ["astaghfirullahalazim"], "أستغفر الله العظيم"),
("jazakallah", ["jazakallahkhair", "jazakallahkhairan", "jzk"], "جزاك الله خيرًا"),
("jazakumullah", ["jazakumullahkhair", "jazakumullahkhairan"], "جزاكم الله خيرًا"),
("barakallah", ["barakallahufeek", "barakallahfeek"], "بارك الله فيك"),
("barakallahufeekum", ["barakallahfeekum"], "بارك الله فيكم"),
("tabarakallah", ["tabarakalah"], "تبارك الله"),
("ameen", ["aameen", "amiin"], "آمين"),
("allahummaameen", ["allahumaameen"], "اللهم آمين"),
("lahawla", ["lahawlawalaquwwata", "lahawlawalaquwwataillabillah"], "لا حول ولا قوة إلا بالله"),
("innalillahi", ["inalillahi", "innalillah", "innalillahiwainnailayhirajiun"], "إنا لله وإنا إليه راجعون"),
("hasbunallah", ["hasbunallahwanimalwakil"], "حسبنا الله ونعم الوكيل"),
("hasbiyallah", ["hasbiallah"], "حسبي الله ونعم الوكيل"),
("audhubillah", ["aoothubillah", "audhubillahiminashaytanirrajim"], "أعوذ بالله من الشيطان الرجيم"),
("rahimahullah", ["rahimahulah"], "رحمه الله"),
("rahimahallah", [], "رحمها الله"),
("allahyarhamu", ["allahyarhamhu"], "الله يرحمه"),
("allahyarhamha", [], "الله يرحمها"),
("yarhamukallah", ["yarhamukallh"], "يرحمك الله"),
("yahdikumullah", ["yahdeekumullah"], "يهديكم الله ويصلح بالكم"),
("radiallahuanhu", ["radiyallahuanhu"], "رضي الله عنه"),
("radiallahuanha", ["radiyallahuanha"], "رضي الله عنها"),
("radiallahuanhum", ["radiyallahuanhum"], "رضي الله عنهم"),
("alayhissalam", ["alaihissalam", "alayhisalam"], "عليه السلام"),
("sallallahualayhiwasallam", ["salallahualayhiwasallam", "sallallahualaihiwasallam", "sawsfull"], "صلى الله عليه وسلم"),
("fiamanillah", ["fiamanallah", "fiamanillah"], "في أمان الله"),
("hayakallah", ["hayyakallah"], "حياك الله"),
("hayakumullah", ["hayyakumullah"], "حياكم الله"),
("akhialkarim", ["akhialkareem"], "أخي الكريم"),
("ukhtialkarima", ["ukhtialkareema"], "أختي الكريمة"),
("wallahi", ["walahi", "wallah"], "والله"),
("allahualam", ["allahuaalam", "wallahualam"], "والله أعلم"),
("eidmubarak", ["eidmubarek"], "عيد مبارك"),
("eidsaid", [], "عيد سعيد"),
("ramadanmubarak", ["ramadhanmubarak"], "رمضان مبارك"),
("ramadankarim", ["ramadankareem", "ramadhankareem"], "رمضان كريم"),
("jumuahmubarak", ["jummahmubarak", "jumamubarak"], "جمعة مباركة"),
("taqabbalallah", ["taqabbalallahuminnawaminkum"], "تقبل الله منا ومنكم"),
("shukran", ["shukranjazilan"], "شكرًا"),
("afwan", [], "عفوًا"),
("marhaba", ["marhaban"], "مرحبًا"),
("ahlanwasahlan", [], "أهلًا وسهلًا"),
("maasalama", ["maassalama", "maasalaama"], "مع السلامة"),
("sabahalkhair", ["sabahalkhayr"], "صباح الخير"),
("masaalkhair", ["masaalkhayr"], "مساء الخير"),
("kayfahaluk", ["kaifhaluk", "kifhalak"], "كيف حالك؟"),
]
used = {"sallahu","sallallahu","salallahu","sallalahu","salalahu","pbuh","saws","jallajalaluh","jalla","jallajalaluhu",
        "bissm","bismillahrahmanrahim","alh","assal","jazak","wac","sha","tabarka","subhan","azza","ld","lt"}
seen2 = set()
phr = []
for i, (t, alts, ar) in enumerate(P, start=1):
    alts = [a for a in dict.fromkeys(alts) if a != t]
    for w in [t] + alts:
        assert w not in used and w not in seen2 and w not in seen and not w.startswith(("s1","s2")), w
        seen2.add(w)
    phr.append({"id": 500 + i, "label": ar, "text": ar, "trigger": t, "aliases": alts})
json.dump({"format": "wmkeyboard-snippets", "version": 2, "appVersion": 0, "appVersionName": "", "snippets": phr},
          open("arabic-phrases.wmsnippets.json", "w"), ensure_ascii=False, indent=2)
print(len(snips), "surah snippets;", len(phr), "phrases")
# a readable list, for checking
with open("list.txt","w") as fh:
    for n, ar, en in S: fh.write(f"{n:>3}  {en:<16} سورة {ar}   (type s{key(en)} or se{key(en)})\n")
    for t, alts, ar in P: fh.write(f"{t:<26} {ar}\n")
