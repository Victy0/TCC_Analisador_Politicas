from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

import re
import unicodedata
from collections import defaultdict
from heapq import nlargest

import nltk
 
from core.steps.auxiliary_token.bad_token import stop_words
from core.steps.auxiliary_token.finality_token import finality_words

#
#  realizar download de tokenizer do nltk caso não esteja instalado na primeira vez em que executar o script desse arquivo
#
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

key_words=['cpf',"email","e-mail","telefone", "telefone","celular","sexo","endereço","cnpj","nome","cidade", "estado","nascimento"]  

#
#  criação básica de tokenizer ajustável usando módulo 're' 
#
def tokenizer(string):
    pattern = r"""\w+\S+\w+|\w+|\d+\.?,?\d+%|[0-9]{1,2}h?:?[0-9]{2}|[#$&\*'"]+"""

    return re.findall(pattern, string)

#
# resumo de texto validando frequência de palavras
# 
def summarizer_text_ranking(raw_text):
    # iniciação de um novo defaultdict pra ranking, aonde cada chave nova gerada irá receber o valor 0, caso a chave não exista
    ranking = defaultdict(int)

    # Preprocessamento do texto
    raw_text = (
        raw_text.replace("R$", " ")
        .replace("$", " ")
        .replace("\n", " ")
        .replace("\t", " ")
        .replace(".", ". ")
        .strip()
    )
    raw_text = unicodedata.normalize("NFKD", raw_text)
    raw_text = " ".join(raw_text.split())

    # tokenization
    tokens = tokenizer(raw_text)
    tokens = [t for t in tokens if t not in stop_words]
    sentence_list = nltk.sent_tokenize(raw_text)

    # se sentenças menor ou igual à 2, não será sumarizado e retornará o texto de entrada
    if len(sentence_list) <= 2:
        return raw_text

    # cálculo da frequência dos tokens (possivelmente será alterado)
    freq = nltk.probability.FreqDist(tokens)

    # ranking de sentenças
    for i, sentence in enumerate(sentence_list):
        for w in [t for t in tokenizer(sentence.lower()) if t not in stop_words]:
            if w in freq:
                ranking[i] += freq[w]
                if w in key_words:
                    ranking[i]+= 1000
                    
    # número de sentenças que geraram o sumário: fixado até 5 (possivelmente será alterado)
    if len(sentence_list) < 10:
        num_max_sentence = len(sentence_list)
    else:
        num_max_sentence = 10

    # recuperação dos índices que obtiveram as maiores pontuações, obedecendo o número delimitador de sentenças recuperadas
    # string '\n\n' indica o fim de uma sentença
    sentences_idx = nlargest(num_max_sentence, ranking, key = ranking.get)
    sumarized_text = "\n\n ".join(
        [sentence_list[j] for j in sorted(sentences_idx)]
    )

    return sumarized_text

#
#   retorno de texto sumarizado em relação as sentenças que contêm as palavras de finalidade
# 
def summarizer_text(raw_text): 

    # Preprocessamento do texto
    raw_text = (
        raw_text.replace("R$", " ")
        .replace("$", " ")
        .replace("\n", " ")
        .replace("\t", " ")
        .replace(".", ". ")
        .strip()
    )
    raw_text = unicodedata.normalize("NFKD", raw_text)
    raw_text = " ".join(raw_text.split())

    # tokenization e recuperação da listagem de senteças
    sentence_list = nltk.sent_tokenize(raw_text)

    # se sentenças menor ou igual à 3, não será sumarizado e retornará o texto de entrada
    if len(sentence_list) <= 3:
        return raw_text  

    sentence_idx_finality = []

    last_i_finality = -1

    # ranking de sentenças
    for i, sentence in enumerate(sentence_list):
        for w in [t for t in tokenizer(sentence.lower()) if t not in stop_words]:
            
            if (last_i_finality != i) and (i not in sentence_idx_finality) and (w in finality_words):
                sentence_idx_finality.append(i)
                last_i_finality = i

    sentence_idx_finality = list(set(sentence_idx_finality) - set(list_idx_of_ignore_distant_senteces(sentence_idx_finality))) 

    sumarized_text = "".join(
        [sentence_list[idx] for idx in sorted(sentence_idx_finality)]
    )

    # Pode retirnar diretamente o texto o entar sumarizar por ranking
    return summarizer_text_ranking(sumarized_text)

#
#   retorn a lista de indexes de sentenças que podem ser removidas devido a estarem em escopo distante das demais
#
def list_idx_of_ignore_distant_senteces(list_idx):

    list_remove = []

    for i, value in enumerate(list_idx):

        before_can_remove = False
        after_can_remove = False

        if i > 0:
            before_can_remove = True if (value - list_idx[i-1]) > 7 else False

        if i < (len(list_idx) - 1):
            after_can_remove = True if (list_idx[i+1] - value) > 7 else False

        if before_can_remove and after_can_remove:
            list_remove.append(i)

    return list_remove
