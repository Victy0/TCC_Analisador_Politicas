import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from goose3 import Goose
from rest_framework.response import Response
import re
from pdfminer import high_level
import requests

#
#  Extrai texto de arquivos 
#
def text_extractor(request, fileId):
    # Obtem os 4 últimos caracteres do url
    exten = request[-4:]

    #Verifica o tipo de arquivo que está sendo provido pela url e decide qual metodo usar 
    if exten == '.pdf':
        r = requests.get(request,allow_redirects=True)
        completeName = os.path.join('files', fileId+'.pdf')
        open(completeName,'wb').write(r.content)
         
        extracted_text ="\n"
        
        resultText = ""
        counter = 0

        # extrai o conteúdo de várias páginas do arquivo PDF
        while extracted_text != "":  
            # high_level.extract_text extrai o texto de uma pagina do arquivo PDF
            extracted_text = high_level.extract_text(completeName, "", [counter],True,'utf-8')

            # Concatena o resultado  anterior com o texto extraido da página atual
            resultText = resultText + extracted_text
            counter = counter + 1

        removeFile(completeName)
        # Verifica se no texto contem a palavra "Política de privacidade"
        if resultText.lower().find("política de privacidade") != -1:
            is_generic = generic_verification(resultText)
            return is_generic,resultText
        else:
            data = "Documento não é uma politica de privacidade" 
            return False, data        
    else :
        g = Goose()
        # Extrai o texto de uma url
        article = g.extract(url = request)
        g.close()
        # Se não der certo a extração pelo goose utilizamos a opção  raw_html do goose e extraimos pelo beautiful soup
        
        if article.cleaned_text == "" or len(article.cleaned_text)< 500 :
            soup = BeautifulSoup(article.raw_html, 'html.parser')
            
            # Verifica se no titulo contem a palavra "Poltica de privacidade"
            if (soup.find("footer") != None) and (soup.find("footer") != -1):
                soup.footer.extract()

            if (soup.find("header") != None) and (soup.find("header") != -1):
                soup.header.extract()

            if (soup.find("style") != None) and (soup.find("style") != -1) :
                soup.style.extract()

            if (soup.find("head") != None) and (soup.find("head") != -1):
                soup.head.extract()

            if (soup.find("script") != None) and (soup.find("script") != -1):
                soup.script.extract()

            if (soup.find("section") != None) and (soup.find("section") != -1):
                soup.section.extract()

            if (soup.find("nav") != None) and (soup.find("nav") != -1): 
                soup.nav.extract()
            text = soup.get_text()
            # Verifica se no texto contem a palavra "Política de privacidade"
            if soup.get_text().lower().find("política de privacidade") != -1:
                
                is_generic=generic_verification(text)
                return is_generic, text
            else:
                data = "Documento não é uma politica de privacidade"
                return False, data  
        else:
            # Verifica se no texto contem a palavra "Política de privacidade"
            if article._cleaned_text.lower().find("política de privacidade") != -1:
                is_generic=generic_verification(article.cleaned_text)
                return is_generic,article.cleaned_text
            else:
                data = "Documento não é uma politica de privacidade"
                return False, data 



#
# remove arquivo criado
#
def removeFile(file):
    if os.path.isfile(file):
        os.remove(file)

#
# Função que verifica se a politica  de privacidade é generica pelo seu tamanho ou por conter um dos termos abaixo
#
def generic_verification(policy):
    especific_data=["cpf","email","e-mail","telefone", "senha","celular","sexo","endereço","cnpj","nome"] 
    
    # Pontos para verificação 
    points = 0
    for data in especific_data: 
        if re.findall(data,policy):
            points = points + 1
            
    if points < 2 or len(policy) < 5000 :
       return  True
    else:
      return False        