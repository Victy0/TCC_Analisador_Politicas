# ANALISADOR DE POLÍTICAS DE PRIVACIDADE

Trabalho de Conclusão de Curso de graduação de Sistemas de Informação da Universidade Federal Fluminense (UFF) Repositório referente a API que processa políticas de privacidade (tanto em PDF quanto em HTML) indicando a finalidade, declarações de dados coletados e se a política analisada é genérica.

Título: Um analisador para a avaliação de políticas de privacidade de acordo com a LGPD para proteção aos dados pessoais 
 - Versão final: fevereiro de 2022

Alunos integrantes:
 - Victor Matheus Pereira de Azevedo
 - Victor Rodrigues Marques

Orientador:
 - José Viterbo Filho

# Documentação

Link para documentação da API: https://documenter.getpostman.com/view/13202167/UVByHA6H

# Conceitos abordados

 - Data scraping 
 - Sumarização 
 - WebSocket

# Requisitos

Python 3.9.7 ou superior

# Instalação

Clonar o repositório:

    git clone https://github.com/Victy0/TCC_Analisador_Politicas

Criar venv:

    py -m venv venv
    
Ativar venv:

    venv/Scripts/activate

Instalar dependências:

    pip install -r requirements/local.txt

Rodar servidor na venv (porta 8000):

    python manage.py runserver 8000

#  Estrutura de diretórios

O projeto se econtra dividido em 5 principais diretórios:

:small_blue_diamond: core: no qual se encontra as requisições e todos os arquivos que irão realizar a análise da política de privacidade. Ressalta que nessa há o subdiretório 'steps', no qual está presente os arquivos com as etapas para análise e o conjunto de tokens auxiliares para o procedimento.

:small_blue_diamond: files: no qual ficará guardado os arquivos .pdf que serão necessários para a análise solicitada (caso se tenha solicitado a análise de um PDF). Ressalta que os arquivos saõ deletados pelo próprio sistema assim que não forem mais necessários.

:small_blue_diamond: privacyPolicyAnalyzer: no qual está presente as configurações do sistema e do django utilizado.

:small_blue_diamond: requirements: no qual está presente as importações requiridas do sistema e que são necessárias serem baixadas pelo 'pip'. Ressalta que dependendo da data em que se está lendo esse registro, algumas dependências podem ter sofrido atualizações.

:small_blue_diamond: socketServer: no qual se econtras as configurações do servidor do socket.io utilizado para a implementação do webSocket. Juntamente com a requisição para incluir sistemas que não possuem suporte a webSocket.

    |____core

        |____steps

            |____auxiliary_token

    |____files

    |____privacyPolicyAnalyzer

    |____requirements

    |____socketServer

# Repositórios relacionados

Repositório com interface web de usuário que consome a API desse repositório: https://github.com/Victormatheus819/TCC_Analisador-_Politicas_Front_End


