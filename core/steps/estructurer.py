import re
from core.steps.auxiliary_token.especific_data_token import especific_data
from core.steps.auxiliary_token.finality_token import finality_words

#
# método que sinaliza termos específicos no texto
#
def sinalize(request):    
    
    # Sinalização dos dados que serão coletados no texto sumarizado focado nas informações de coleta 
    for word in especific_data:
        compiled = re.compile(re.escape(" " + word + " "), re.IGNORECASE)
        request["coleta"] = compiled.sub(" <b class='sinalizer'>" + word + "</b> ",  request["coleta"])
        request["finalidade"] = compiled.sub(" <b class='sinalizer'>" + word + "</b> ", request["finalidade"])
        
        compiled = re.compile(re.escape(" " + word + ", "), re.IGNORECASE)
        request["coleta"] = compiled.sub(" <b class='sinalizer'>" + word + "</b>, ", request["coleta"])
        request["finalidade"] = compiled.sub(" <b class='sinalizer'>" + word + "</b>, ", request["finalidade"])
        
        compiled = re.compile(re.escape(" " + word + "."), re.IGNORECASE)
        request["coleta"] = compiled.sub(" <b class='sinalizer'>" + word + "</b>.", request["coleta"])
        request["finalidade"] = compiled.sub(" <b class='sinalizer'>" + word + "</b>.", request["finalidade"])
    
    request["coleta"] = request["coleta"].replace("\n","<br>") 
    
    # Sinalização dos dados que serão coletados no texto sumarizado focado nas finalidades de uso de dados
    for word in finality_words:
        compiled = re.compile(re.escape(" " + word + " "), re.IGNORECASE)
        request["finalidade"] = compiled.sub(" <b class='sinalizer'>" + word + "</b> ", request["finalidade"])
        
        compiled = re.compile(re.escape(" " + word + ", "), re.IGNORECASE)
        request["finalidade"] = compiled.sub(" <b class='sinalizer'>" + word + "</b>, ", request["finalidade"])
        
        compiled = re.compile(re.escape(" " + word + "."), re.IGNORECASE)
        request["finalidade"] = compiled.sub(" <b class='sinalizer'>" + word + "</b>.", request["finalidade"])

    request["finalidade"] = request ["finalidade"].replace("\n","<br>") 
    
    return request
