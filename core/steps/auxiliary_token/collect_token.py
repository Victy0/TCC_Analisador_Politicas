from string import punctuation

terms=[
    "coletamos",
    "coletaremos",
    "coleta",
    "coletar",
    "coletados",
    "coletadas",
    "recolher",
    "recolhidas",
    "recolhidos",
    "gravar",
    "indicada",
    "indicados",
    "fornecidos",
    "fornecer",
    "solicitamo",
    "solicitar",
    "solicitadas",
    "solicitados",
    "solicitado",
    "solicitada",
    "poderá",
]

punctuation = punctuation.replace('"', "").replace("'", "")

terms.extend(list(punctuation))

collect_words = set(terms)

del terms