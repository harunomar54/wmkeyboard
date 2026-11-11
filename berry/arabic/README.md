# Quran and Hadith predictions for Arabic

`build_quran_hadith.py` writes two AOSP `.combined` dictionaries for
Typing › Suggestions › Custom dictionaries (language: Arabic). Each carries its
words plus word pairs and triples, so next-word prediction walks through an
ayah or a hadith one word at a time.

- `quran-ar.combined`: the Quran, Tanzil "simple" text with vowel marks
  removed and hamza forms kept. Ayahs run on into the next within a surah.
- `hadith-ar.combined`: the matn of Sahih al-Bukhari and Sahih Muslim, taken
  as the text after the first "صلى الله عليه وسلم"; narrations without it are
  left out.

Sources:
- Quran text: Tanzil Project (https://tanzil.net), CC BY 3.0, via
  fawazahmed0/quran-api edition `ara-quransimple`.
- Hadith text: fawazahmed0/hadith-api editions `ara-bukhari` and `ara-muslim`.

    python3 build_quran_hadith.py <folder with the four json files> <output folder>
