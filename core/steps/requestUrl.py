from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from goose3 import Goose
from rest_framework.response import Response

from pdfminer import high_level
import requests

def textExtractor (request):
    exten = request[-4:]
    print(exten)

    if exten == '.pdf':
        r= requests.get(request,allow_redirects=True)

        open('Analised.pdf','wb').write(r.content)
     
        local_pdf_filename = "Analised.pdf"
       
        extracted_text ="\n"
        
        resultText = ""
        counter= 0
        while extracted_text != "":  
            extracted_text = high_level.extract_text(local_pdf_filename, "", [counter],True,'utf-8')
            resultText.join(extracted_text)
            
            counter= counter+1
            print(counter)
        return resultText
     
    else :
        g = Goose()
        article = g.extract(url=request)
        g.close()
        if article.cleaned_text == "":
            soup = BeautifulSoup(article.raw_html, 'html.parser')
            return soup.get_text()
        else:
            return article.cleaned_text


    