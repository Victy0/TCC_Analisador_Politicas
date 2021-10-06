import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from goose3 import Goose
from rest_framework.response import Response

from pdfminer import high_level
import requests

#
#  Extrai texto de arquivos 
#
def textExtractor (request, fileId):
    # Obtem os 4 ultimos caracteres do url
    exten = request[-4:]
    #Verifica o tipo de arquivo que está sendo provido pela url e decide qual metodo usar 
    if exten == '.pdf':
        r= requests.get(request,allow_redirects=True)
        completeName= os.path.join('files', fileId+'.pdf')
        open(completeName,'wb').write(r.content)
         
        extracted_text ="\n"
        
        resultText = ""
        counter= 0
        while extracted_text != "":  
            # high_level.extract_text extrai o texto de uma pagina do arquivo pdf
            extracted_text = high_level.extract_text(completeName, "", [counter],True,'utf-8')
            # Concatena o resultado  anterior com o texto extraido da pagina atual
            resultText= resultText + extracted_text
            counter= counter+1
        removeFile(completeName)  
        return resultText
     
    else :
        g = Goose()
        # Extrai o texto de uma url
        article = g.extract(url=request)
        g.close()
        # Se não der certo a extração pelo goose utilizamos a opção  raw_html do goose e extraimos pelo beautiful soup
        if article.cleaned_text == "":
            soup = BeautifulSoup(article.raw_html, 'html.parser')
            return soup.get_text()
        else:
            return article.cleaned_text

def removeFile(file):
 if os.path.isfile(file):
    os.remove(file)      
    