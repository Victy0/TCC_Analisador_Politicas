import re

#
# método que sinaliza termos específicos no texto
#
def sinalize (request):
    payload = {
        'text':'',
        'politica_generica':False
        }
    
    # Array de palavras a serem sinalizadas     
    subwords = ["cpf","email","e-mail","telefone", "senha","celular","sexo","endereço","cnpj","nome"]
    text = request
    for word in subwords:
        compiled = re.compile(re.escape(word), re.IGNORECASE)
        text = compiled.sub("<b>" + word + "</b>",  text)
    
    text = text.replace("\n","<br>") 
    payload['text']= text
    
    # Array para verificação para texto generico
    especific_data=["cpf","email","e-mail","telefone", "senha","celular","sexo","endereço","cnpj","nome"] 
    
    # Pontos para verificação 
    points = 0
    for data in especific_data: 
        if re.findall(data,text):
            points = points + 1
            
    if points == 0:
        payload['politica_generica'] = True
    else:
        payload['politica_generica'] = False  
    
    return payload
