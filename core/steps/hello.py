from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from goose3 import Goose
from rest_framework.response import Response

def helloFriend ():
    g = Goose()
    article = g.extract(url='https://www.paodeacucar.com/user/register')
    g.close()
    if article.cleaned_text == "":
        soup = BeautifulSoup(article.raw_html, 'html.parser')
        return soup.get_text()
    else:
        return article.cleaned_text
    