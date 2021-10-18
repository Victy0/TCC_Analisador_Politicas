from string import punctuation


terms=[
    "utilizará",
    "utilizado",
    "utilizados",
    "utilizadas",
    "utilizada",
    "utilizar",
    "usa",
    "usar",
    "usados",
    "usadas",
    "usado",
    "usada",
    "finalidade",
    "finalidades",
    "fins",
    "propósito",
    "propósitos",
    "fornecer",
    "fornecimento",
    "atualizar",
    "manter" ,
    "proteger",
    "intuito",
    "enviar",
    "envio",
    "customizar",
    "customização",
    "exibe",
    "exibir",
    "conduzir",
    "condução",
    "investigar ",
    "investigação",
    "análises",
    "análise",
    "tratar",
    "tratamos",
    "tratados",
    "tratadas",
    "tratamento",
    "identificar",
    "identificação",
    "autenticar",
    "autenticação",
    "transferir",
    "transferência",
    "transferidos",
    "ampliar",
    "ampliação",
    "realizar ",
    "realize",
    "realização",
    "compartilhar",
    "compartilhamento",
    "agendar",
    "agendamento",
    "processados",
    "sistematização",
    "aprimorar",
    "aprimoramento",
    "proporcionar",
    "auditoria",
    "auditorias",
    "personalizar",
    "agilizar",
    "facilitar",
    "viabilizar",
    "viabilização",
    "comercializar ",
    "registrar",
    "realizar",
    "testar",
    "corrigir ",
    "correção",
    "gerenciar",
    "gerenciamento",
    "evitar",
    "cumprir",
    "cumprimento",
    "aperfeiçoar",
    "aperfeiçoamento",
    "refutar",
    "promover",
    "promoção",
    "resguardar",
    "resguardo",
    "colaborar",
    "colaboração",
    "prosseguir ",
    "prosseguimento",
    "consulta",
    "consultar",
    "valorizar",
    "divulgação",

]

punctuation = punctuation.replace('"', "").replace("'", "")

terms.extend(list(punctuation))

finality_words = set(terms)

del terms