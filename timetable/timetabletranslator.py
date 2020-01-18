lt_dl = ["Paskaita", "Grupė", "Laikas", "Savaitė", "Pogrupis",
         "Dalykas", "Auditorija", "Dėstytojas", "Tipas", ]

en_dl = ["Lecture", "Group", "Time", "Week", "Subgroup",
         "Subject", "Auditory", "Lecturer", "Type", ]

tags_dl = ["lecture", "group", "time", "week", "subgroup",
           "subject", "auditory", "lecturer", "type"]

data_label_translations = {
    "en": dict(zip(tags_dl, en_dl)),
    "lt": dict(zip(tags_dl, lt_dl))
}


lt_dow = ["Pirmadienis", "Antradienis", "Trečiadienis",
          "Ketvirtadienis", "Penktadienis", "Šeštadienis", "Sekmadienis"]

en_dow = ["Monday", "Tuesday", "Wednesday",
          "Thursday", "Friday", "Saturday", "Sunday"]

tags_dow = range(7)

dow_translations = {
    "en": dict(zip(en_dow, tags_dow)),
    "lt": dict(zip(lt_dow, tags_dow))
}
