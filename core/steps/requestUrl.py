import os
from bs4 import BeautifulSoup
from goose3 import Goose
import re
from pdfminer import high_level
import requests
from core.steps.auxiliary_token.especific_data_token import especific_data
import tabula



#
#  Extrai texto de arquivos 
#
def text_extractor(request, file_id):
    # Obtem os 4 últimos caracteres da url
    exten = request[-4:]

    result_text = ""

    # Verifica o tipo de arquivo se é PDF e extrai do PDF
    if exten == '.pdf':
        del exten
        # baixar arquivo PDF
        r = requests.get(request, allow_redirects=True)
        complete_name = os.path.join('files', file_id + '.pdf')
        open(complete_name,'wb').write(r.content)
         
        extracted_text ="\n"
        
        counter = 0 
        
        # extrai o conteúdo de várias páginas do arquivo PDF
        while extracted_text != "":  
            # high_level.extract_text extrai o texto de uma pagina do arquivo PDF
            extracted_text = high_level.extract_text(complete_name, "", [counter],True,'utf-8')

            if extracted_text != "":
                # extração de tabelas da página atual 
                tables = tabula.read_pdf(complete_name, pages = [counter+1], output_format="json")

                for table in tables:
                    page_text, first_text, last_text = agroup_table(table)
                    extracted_text=extracted_text.replace("\n", "")
                    # remove a tabela do texto extraido e coloca a tabela formatada caso seja realmente uma tabela
                    if page_text != None:
                        test_1 = extracted_text[0 : extracted_text.find(first_text)]
                        test_2 = extracted_text[(extracted_text.find(last_text) + len(last_text)) :]
                        extracted_text = ( test_1 ) + ( page_text ) + ( test_2 )

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
            com = []
            for idx_row, row in enumerate(table.find_all("tr")):
                col_list = row.find_all("td")
                
                # agrupa o valor de todas as linhas na posição da coluna em que se encontra
                for idx_col, actual_col in enumerate(col_list):

                    # insere novo índice no array referente a coluna da tabela não mapeada
                    if idx_row == 0:
                        com.append("")

                    for idx_content, content in enumerate(actual_col.contents):

                        # se o valor recuperado for uma tag, recupera a string do mesmo
                        content = content if content.string == None else content.string
                        com[idx_col] = com[idx_col] + str(content).replace('.', ';')

                        # colocar ': ' após o final de um header da tabela
                        if (idx_content == len(actual_col.contents) - 1) and (idx_row == 0):
                            com[idx_col] = com[idx_col] + ': '

            table_str = '. '.join(str(e) for e in com)

        # Se não der certo a extração pelo goose, é extraido pelo beautiful soup
        if article.cleaned_text == "" or len(article.cleaned_text) < 500 :
            
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
   
    
    # Pontos para verificação 
    points = 0
    for data in especific_data: 
        if re.findall(" " + data, policy):
            points = points + 1
    del data       
    if points < 8 or len(policy) < 5000 :
        del points
        return  True
    else:
      del points
      return False        

#
# Retira texto das tabelas contidas em um pdf e os agrupa em strings
#
def agroup_table(table):
  
    array= []
    last_text= ""
    first_text=""

    
    for index_rows, rows in enumerate(table["data"]):

        if len(rows) == 1:
            return None, None, None

        for index_position, position in enumerate(rows):
            if index_rows == 0:
                array.append("")
            if position["text"] != "" : 
                if first_text == "" :
                    first_text = position["text"] 
                array[index_position] = array[index_position] + " " + position["text"]    
        
    if len(array[-1]) > 3:
        words = array[-1].split(" ")
        last_text = words[-5]+ " "+ words[-4]+ " " + words[-3] + " " + words[-2] + " " + words[-1]
    else:
        last_text = array[-1]

    table_str = '. '.join(str(e).replace('.',';') for e in array) 
    
   
    return ' '.join(dict.fromkeys(table_str.split())), first_text, last_text