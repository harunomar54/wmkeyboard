# Names (BB-Keyboard)

What makes a typed name such as `bilal` or `abdurahman` come out as
`Bilal` or `Abdurahman`.

- `arabic_names.txt` is a hand list of Arabic, Somali, South Asian, Turkish
  and Persian Muslim given names, with the spellings people use for them. It
  also has the Abd- compounds, the prophets, the Sahaba and the proper nouns
  of the faith.
- `exclude.txt` lists everyday words in English or Muslim English that must
  stay lower case: said, dua, iman, ameen and so on.
- `../tools/build_names.py` combines the hand list with the US Social Security
  baby names. It drops the following:
  - anything that is an ordinary English word, checked against AOSP's
    frequencies and Webster's;
  - likely misspellings of a common word or a common name;
  - US names with fewer than 300 births.

  The **Berry data** workflow runs it. Its output is appended to
  `app/src/main/assets/dictionaries/en_caps.txt`, which ships in the app.
- `report.txt` is what the last run kept and turned away, and why.
- `names-en-ar.combined` is an optional extra dictionary of the same names. It
  is not needed for capitals. Import it in Settings, Custom dictionaries, so
  the strip also offers and completes names (bil... becomes Bilal), and so
  swiping works on them.
