# -*- coding: utf-8 -*-
from benchmarkit import benchmark

from similaridade.levenshtein import Levenshtein


class Jaccard:

    """
    Algoritmo de similaridade - Jaccard
    """
    @staticmethod
    @benchmark()
    def similaridade_jaccard(t1, t2):
        # Simplificação dos textos de entrada
        t1 = Levenshtein.limpar_texto(t1)
        t2 = Levenshtein.limpar_texto(t2)

        # Exibe o número de caracteres de cada texto após a simplificação
        #print('Tamanho do texto1: ', len(t1))
        #print('Tamanho do texto2: ', len(t2))
        #print('')

        # Separa os dois textos em listas com frases. Os sinais de ? e ! foram convertidos em .
        trechos1 = t1.split('. ')
        trechos2 = t2.split('. ')

        # Exibe a quantidade de frases de cada texto
        #print('Quantidade de frases do texto1: ', len(trechos1))
        #print('Quantidade de frases do texto2: ', len(trechos2))
        #print('')

        # Esta lista irá a armazenar a quantidade de palavras e o percentual de similaridade de cada frase do texto 1
        lista_similaridade = []

        # Loop que fará a comparação de cada frase do texto1
        for i in range(0, len(trechos1)):

            palavras1 = trechos1[i].split()
            qt_palavras1 = len(palavras1)
            qt_palavras2 = 0
            max_indice_jaccard = 0
            posicao_j = 0

            # Exibe cada frase do texto1 antes de compará-la às frases do texto2
            #print(trechos1[i])

            # Loop que fará a comparação com cada frase do texto2
            for j in range(0, len(trechos2)):

                palavras2 = trechos2[j].split()
                indice_jaccard = Jaccard.similaridade_trecho_jaccard(palavras1, palavras2)

                # Se o índice jaccard encontrada for maior que o índice mínimo:
                # A frase do texto2 corrente possui uma similaridade melhor com a frase do texto1
                # Nesta situação, devemos guardar os valores encontrados
                if indice_jaccard > max_indice_jaccard:
                    max_indice_jaccard = indice_jaccard
                    posicao_j = j

            # Ao percorrer todas as frases do texto2, podemos identificar qual delas possui maior similaridade com o texto1
            # Calcula-se o percentual de similaridade entre as duas frases
            percent_similaridade = 0
            if qt_palavras1 > 0:
                #percent_indice = (max_indice_jaccard / qt_palavras1) * 100
                #percent_similaridade = 100 - percent_indice
                percent_similaridade = max_indice_jaccard * 100

            # Exibição da frase do texto2 que possui maior similaridade com o texto1
            #print('Frase com maior similaridade:')
            #print(trechos2[posicao_j])

            # Exibição do Maior Índice Jaccard entre as duas frases do texto1 e texto2
            #print('Maior Índice Jaccard: ', max_indice_jaccard)

            # Exibição do percentual de similaridade entre as duas frases
            #print('Percentual de similaridade: ', percent_similaridade)
            #print('')

            # Os valores qt_palavras1 e percent_similaridade são armazenados na lista de similaridades
            lista_similaridade.append([qt_palavras1, percent_similaridade])

        # Calcula-se a média ponderada dos valores armazenados na lista de similaridades:
        # Para cada frase do texto1, temos armazenados (qt_palavras1 e percent_similaridade)
        # Percorremos a lista e calculamos a média ponderada destes valores para obter a similaridade total entre os textos
        peso = 0
        soma = 0
        for i in range(0, len(lista_similaridade)):
            peso = peso + lista_similaridade[i][0]
            soma = soma + (lista_similaridade[i][0] * lista_similaridade[i][1])
        similaridade = 0
        if peso > 0:
            similaridade = soma / peso
        print('')

        # Exibe a lista de similaridades
        #print('Lista de similaridades: ', lista_similaridade)

        # Exibe a similaridade total entre os texto1 e texto2
        #print('Similaridade total entre os textos: ', similaridade)
        return similaridade

    @staticmethod
    @benchmark()
    def similaridade_jaccard_original(t1, t2):
        palavras1 = t1.split()
        palavras2 = t2.split()
        indice_jaccard = Jaccard.similaridade_trecho_jaccard(palavras1, palavras2)
        return indice_jaccard * 100


    #
    @staticmethod
    def similaridade_trecho_jaccard(a, b):
        union = list(set(a + b))
        intersection = list(set(a) - (set(a) - set(b)))
        return float(len(intersection)) / len(union)

