from ttdatatags import tags

def to_data_label_tag(data_label):
    for ltags in language_tags:
        if data_label in ltags:
            return ltags[data_label]

en = []
en_tags = dict(zip(en, tags))

lt = [
    "Paskaita",
    "Grupė",
    "Laikas",
    "Savaitė",
    "Pogrupis",
    "Dalykas",
    "Auditorija",
    "Dėstytojas",
    "Tipas",
]
lt_tags = dict(zip(lt, tags))

language_tags = [en_tags, lt_tags]