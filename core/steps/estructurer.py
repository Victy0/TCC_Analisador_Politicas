import re
from core.steps.auxiliary_token.especific_data_token import especific_data

#
# método que sinaliza termos específicos no texto
#
def sinalize (request):
   
    
    # Array de palavras a serem sinalizadas     
    
    # Sinalização dos dados que serão coletados no texto sumarizado focado nas informações de coleta 
    for word in especific_data:
        compiled = re.compile(re.escape(" "+word), re.IGNORECASE)
        request["coleta"] = compiled.sub("<b>" + " "+word + "</b>",  request["coleta"])
    
    request["coleta"] = request["coleta"].replace("\n","<br>") 
    
     # Sinalização dos dados que serão coletados no texto sumarizado focado nas finalidades de uso de dados
    for word in especific_data:
        compiled = re.compile(re.escape(" "+word), re.IGNORECASE)
        request["finalidade"] = compiled.sub("<b>" +" "+ word + "</b>", request["finalidade"])
    request ["finalidade"] = request ["finalidade"].replace("\n","<br>") 
    
    return request
