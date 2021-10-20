import re

#
# método que sinaliza termos específicos no texto
#
def sinalize (request):
   
    
    # Array de palavras a serem sinalizadas     
    subwords = ["cpf","email","e-mail","telefone", "senha","celular","sexo","endereço","cnpj","nome"]
    
    for word in subwords:
        compiled = re.compile(re.escape(word), re.IGNORECASE)
        request["coleta"] = compiled.sub("<b>" + word + "</b>",  request["coleta"])
    
    request["coleta"] = request["coleta"].replace("\n","<br>") 
    
    for word in subwords:
        compiled = re.compile(re.escape(word), re.IGNORECASE)
        request["finalidade"] = compiled.sub("<b>" + word + "</b>", request["finalidade"])
    request ["finalidade"] = request ["finalidade"].replace("\n","<br>") 
    
    
    # Array para verificação para texto generico
    # especific_data=["cpf","email","e-mail","telefone", "senha","celular","sexo","endereço","cnpj","nome"] 
    
    # # Pontos para verificação 
    # points = 0
    # for data in especific_data: 
    #     if re.findall(data,text):
    #         points = points + 1
            
    # if points == 0:
    #     payload['politica_generica'] = True
    # else:
    #     payload['politica_generica'] = False  
    
    return request
