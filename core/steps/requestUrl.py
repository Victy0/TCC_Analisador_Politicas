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
        resultText=resultText.lower()
        
        if resultText.find("política de privacidade")!=-1:
           
            return resultText
        else:
            data="Documento não é uma politica de privacidade" 
            return data   
        
     
    else :
        g = Goose()
        # Extrai o texto de uma url
        article = g.extract(url=request)
        g.close()
        # Se não der certo a extração pelo goose utilizamos a opção  raw_html do goose e extraimos pelo beautiful soup
        
        if article.cleaned_text == "" or len(article.cleaned_text)< 500 :
            soup = BeautifulSoup(article.raw_html, 'html.parser')
            if  "Privacidade" in soup.title.contents[0]:
                if soup.find("footer")!= None and soup.find("footer")!=-1:
                    soup.footer.extract()
                if soup.find("header")!= None and soup.find("header")!=-1:
                    soup.header.extract()    
                if soup.find("style")!= None  and  soup.find("style")!= -1 :
                    soup.style.extract()
                if soup.find("head")!= None and  soup.find("head")!= -1:
                    soup.head.extract()    
                if soup.find("script")!= None and soup.find("script")!=-1:
                    soup.script.extract()
                if soup.find("section")!= None and soup.find("section")!=-1:
                    soup.section.extract()
                if soup.find("nav")!= None  and soup.find("nav")!=-1: 
                    soup.nav.extract()
                text=soup.get_text()
                return text
            else:
                data="Documento não é uma politica de privacidade"
                return data  
        else:
            article.cleaned_text=article._cleaned_text.lower()
            if article._cleaned_text.find("política de privacidade") !=-1:
                return article.cleaned_text
            else:
                data="Documento não é uma politica de privacidade"
                return data 

def removeFile(file):
 if os.path.isfile(file):
    os.remove(file)      