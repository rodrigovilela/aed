import re
from hashlib import blake2b

class ProcessadorTexto():

    @staticmethod
    def extrair_trechos(texto):
        '''
        :param texto: Texto composto por parágrafos/frases que serão quebradas em trechos.
        Cada trecho é a uma frase terminada em ponto final.
        :return: array com os trechos identificados.
        '''
        texto = re.sub(r'<.*?>', ' ', texto)
        texto = re.sub(r'[^\sça-zA-Z|^-|^\_|^\?|^\!|^\;|^.|^á|^é|^í|^ó|^ú|^â|^ê|^ô|^ã|^õ]', ' ', texto)
        texto = re.sub(r'\d+', '', texto)
        texto = re.sub(r'[\?|\!|\;]', '.', texto)
        texto = re.sub(r'\W*\b\w{1,3}\b', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)

        trechos = texto.split(".")
        trechos_validos = []
        for trecho in trechos:
            trecho = trecho.strip()
            if len(trecho) > 3 and len(trecho.split()) > 5:
                trechos_validos.append(trecho.lower())

        return trechos_validos

    @staticmethod
    def gerar_hash(trecho):
        '''
        Aplica função hash definida em https://docs.python.org/3/library/hashlib.html
        :param texto: trecho correspondente a uma frase.
        :return: hash do trecho.
        '''
        h = blake2b(digest_size=12)
        trecho = trecho.encode('utf-8')
        h.update(trecho)
        return h.hexdigest()
