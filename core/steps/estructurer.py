
import re
import json


def Sinalize (request):
    payload ={
        'text':'',
        'flag':False
        }
    subwords=['CPF',"EMAIL","E-MAIL","TELEFONE", "SENHA","CELULAR","SEXO","ENDEREÇO","EMAIL","CNPJ","NOME","FINALIDADE","DADOS","FINS"]
    text=request
    for word in subwords:
        compiled = re.compile(re.escape(word), re.IGNORECASE)
        text = compiled.sub("<b>" + word + "</b>",  text)
    
    text=text.replace("\n","<br>") 
    payload['text']= text
    
    especificdata=['CPF',"EMAIL","E-MAIL","TELEFONE", "SENHA","CELULAR","SEXO","ENDEREÇO","EMAIL","CNPJ","NOME"] 
    
    points=0
    for data in especificdata: 
        if re.findall(data,text):
            points= points+1
    if points==0:
        payload['flag']= True
    else:
          payload['flag']= False  
    
     
    
    return payload
