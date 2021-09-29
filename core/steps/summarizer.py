from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer


def sumarizationText(rawText):
    parser = PlaintextParser.from_string(rawText, Tokenizer('portuguese'))
    summarizer = LuhnSummarizer()
    # número de sentenças fixado em 5
    sentenceList = summarizer(parser.document, 5)

    return '. '.join(str(e) for e in sentenceList)