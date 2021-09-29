from string import punctuation

terms = [
    "de",
    "a",
    "o",
    "que",
    "e",
    "do",
    "da",
    "em",
    "um",
    "para",
    "com",
    "uma",
    "os",
]

punctuation = punctuation.replace('"', "").replace("'", "")

terms.extend(list(punctuation))

stop_words = set(terms)

del terms