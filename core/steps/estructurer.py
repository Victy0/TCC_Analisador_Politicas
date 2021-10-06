
import re


def Sinalize (request):
    subwords=['CPF',"EMAIL","TELEFONE", "SENHA","CELULAR","SEXO","ENDEREÇO","EMAIL","CNPJ","NOME","FINALIDADE","DADOS","FINS"]
    text=request
    for word in subwords:
        compiled = re.compile(re.escape(word), re.IGNORECASE)
        text = compiled.sub("<b>" + word + "</b>",  text)
    
    text=text.replace("\n","<br>")    
    return text
