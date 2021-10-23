import os
from bs4 import BeautifulSoup
from goose3 import Goose
import re
from pdfminer import high_level
import requests



#
#  Extrai texto de arquivos 
#
def text_extractor(request, file_id):
    # Obtem os 4 últimos caracteres da url
    exten = request[-4:]

    result_text = ""

    # Verifica o tipo de arquivo se é PDF e extrai do PDF
    if exten == '.pdf':

        r = requests.get(request,allow_redirects=True)
        complete_name = os.path.join('files', file_id+'.pdf')
        open(complete_name,'wb').write(r.content)
         
        extracted_text ="\n"
        
        counter = 0

        # extrai o conteúdo de várias páginas do arquivo PDF
        while extracted_text != "":  
            # high_level.extract_text extrai o texto de uma pagina do arquivo PDF
            extracted_text = high_level.extract_text(complete_name, "", [counter],True,'utf-8')

            # Concatena o resultado  anterior com o texto extraido da página atual
            result_text = result_text + extracted_text
            counter = counter + 1

        # remove arquivo PDF após a extração
        remove_file(complete_name)   

    # Extração de página HTML 
    else :

        # instância goose e extração
        g = Goose()
        article = g.extract(url = request)
        g.close()

        # instância do beautifulSoup pela opção raw_html do goose
        soup = BeautifulSoup(article.raw_html, 'html.parser')

        # extração dados de tabela
        table_list = soup.find_all("table")
        table_str = ""

        for table in table_list:
            idx_aux = -1
            com = []
            for row in table.find_all("tr"):
                col_list = row.find_all("td")

                # foram array com as quantidade específica de colunas da tabela 
                if(idx_aux == -1):
                    for idx_c in range(len(col_list[0].contents)):
                        com.append("")
                    idx_aux = 0
                
                # agrupa o valor de todas as linhas na posição da coluna em que se encontra
                for idx, actual_col in enumerate(col_list):
                    for content in actual_col.contents:

                        # se o valor recuperado for uma tag, recupera a string do mesmo
                        content = content if content.string == None else content.string
                        com[idx] = com[idx] + str(content).replace('.', ';')
            
            table_str = ''.join(str(e) for e in com)

        # Se não der certo a extração pelo goose, é extraido pelo beautiful soup
        if article.cleaned_text == "" or len(article.cleaned_text)< 500 :
            
            # Remove tags desnecessárias para extração
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

            if (soup.find("nav") != None) and (soup.find("nav") != -1): 
                soup.nav.extract()

            if(soup.find("table") != None) and (soup.find("table") != -1):
                soup.table.extract()

            result_text = soup.get_text() + table_str

        else:
            result_text = article.cleaned_text + table_str

        # Verifica se no texto contem a palavra "Política de privacidade"
        if result_text.lower().find("política de privacidade") != -1:
            is_generic = generic_verification(result_text)
            return is_generic, result_text
        else: 
            return False, "Sistema considerou o documento como não sendo uma política de privacidade" 



#
# remove arquivo criado
#
def remove_file(file):
    if os.path.isfile(file):
        os.remove(file)



#
# Função que verifica se a política de privacidade é genérica pelo seu tamanho ou por não conter um dos termos específicos
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