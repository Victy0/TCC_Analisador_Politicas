from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

import re
import unicodedata
from collections import defaultdict
from heapq import nlargest

import nltk
 
from core.steps.auxiliary_token.bad_token import stop_words

#
#  realizar download de tokenizer do nltk caso não esteja instalado na primeira vez em que executar o script desse arquivo
#
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

#
#  resumo básico de texto 
#
def basic_summarizer_text(raw_text):
    parser = PlaintextParser.from_string(raw_text, Tokenizer('portuguese'))
    summarizer = LuhnSummarizer()
    # número de sentenças fixado em 5
    sentence_list = summarizer(parser.document, 5)

    return '. '.join(str(e) for e in sentence_list)

#
#  criação básica de tokenizer ajustável usando módulo 're' 
#
def tokenizer(string):
    pattern = r"""\w+\S+\w+|\w+|\d+\.?,?\d+%|[0-9]{1,2}h?:?[0-9]{2}|[#$&\*'"]+"""

    return re.findall(pattern, string)

#
# resumo de texto validanco frequência de palavras
# 
def summarizer_text(raw_text):
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

    # a primeira sentença sempre irá ser retornada. Para isso foi jogado um valor de ranking elevado para garantir sempre a primeira posição na lista de ranking
    ranking[0] = 10000000000

    for i, sentence in enumerate(sentence_list):
        for w in tokenizer(sentence.lower()):
            if w in freq:
                ranking[i] += freq[w]

    # número de sentenças que geraram o sumário: fixado até 5 (possivelmente será alterado)
    if len(sentence_list) < 5:
        num_max_sentence = len(sentence_list)
    else:
        num_max_sentence = 5

    # recuperação dos índices que obtiveram as maiores pontuações, obedecendo o número delimitador de sentenças recuperadas
    # string '\n\n' indica o fim de uma sentença
    sentences_idx = nlargest(num_max_sentence, ranking, key = ranking.get)
    sumarized_text = "\n\n ".join(
        [sentence_list[j] for j in sorted(sentences_idx)]
    )

    return sumarized_text

    