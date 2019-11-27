# -*- coding: utf-8 -*-
import numpy as np
from benchmarkit import benchmark


class Levenshtein:

    """
    Algoritmo de similaridade - Levenshtein
    """

    # Calcula a distância de Leventheins comparando palavras entre frases
    @staticmethod
    def levenshtein_palavra(s1, s2):
        l1 = s1.split(' ')
        l2 = s2.split(' ')
        # print(l1)
        # print(l2)
        m = len(l1) + 1
        n = len(l2) + 1

        matriz = np.zeros((m, n))

        for i in range(0, m):
            matriz[i][0] = i

        for i in range(0, n):
            matriz[0][i] = i

        for i in range(1, m):
            for j in range(1, n):
                if l1[i - 1] == l2[j - 1]:
                    matriz[i, j] = min(
                        matriz[i - 1, j] + 1,
                        matriz[i - 1, j - 1],
                        matriz[i, j - 1] + 1
                    )
                else:
                    matriz[i, j] = min(
                        matriz[i - 1, j] + 1,
                        matriz[i - 1, j - 1] + 1,
                        matriz[i, j - 1] + 1
                    )
        # print(matriz)
        distancia = (matriz[m - 1, n - 1])
        # print('Tamanho texto1: ', m - 1)
        # print('Tamanho texto2: ', n - 1)
        # print('Distância de Levenshtein: ', distancia)
        return distancia, m-1, n-1


    # Remove acentos do texto
    @staticmethod
    def remover_acentos(texto):
        texto = texto.replace('á', 'a')
        texto = texto.replace('à', 'a')
        texto = texto.replace('ã', 'a')
        texto = texto.replace('é', 'e')
        texto = texto.replace('ê', 'e')
        texto = texto.replace('í', 'i')
        texto = texto.replace('ó', 'o')
        texto = texto.replace('ô', 'o')
        texto = texto.replace('õ', 'o')
        texto = texto.replace('ú', 'u')
        texto = texto.replace('ü', 'u')
        return texto


    # Remove caracteres especiais do texto
    @staticmethod
    def remover_caracteres_especiais(texto):
        texto = texto.replace('-', '')
        texto = texto.replace('ª', '')
        texto = texto.replace('º', '')
        texto = texto.replace('#', '')
        texto = texto.replace('"', '')
        texto = texto.replace("'", '')
        texto = texto.replace('<', '')
        texto = texto.replace('>', '')
        texto = texto.replace('(', '')
        texto = texto.replace(')', '')
        texto = texto.replace('‘', '')
        texto = texto.replace('’', '')
        texto = texto.replace('“', '')
        texto = texto.replace('”', '')
        texto = texto.replace('/', '')
        return texto


    # Remove sinais de pontuação e substitui ? e ! por .
    @staticmethod
    def remover_sinais_pontuacao(texto):
        texto = texto.replace(',', '')
        texto = texto.replace(';', '')
        texto = texto.replace(':', '')
        texto = texto.replace('?', '.')
        texto = texto.replace('!', '.')
        return texto


    # Remove palavras simples: artigos, preposições, etc
    @staticmethod
    def remover_palavras_simples(texto):
        texto = texto.replace(' a ', ' ')
        texto = texto.replace(' e ', ' ')
        texto = texto.replace(' o ', ' ')
        texto = texto.replace(' ao ', ' ')
        texto = texto.replace(' da ', ' ')
        texto = texto.replace(' de ', ' ')
        texto = texto.replace(' do ', ' ')
        texto = texto.replace(' das ', ' ')
        texto = texto.replace(' dos ', ' ')
        texto = texto.replace(' em ', ' ')
        texto = texto.replace(' na ', ' ')
        texto = texto.replace(' no ', ' ')
        texto = texto.replace(' nas ', ' ')
        texto = texto.replace(' nos ', ' ')
        texto = texto.replace(' um ', ' ')
        texto = texto.replace(' uns ', ' ')
        texto = texto.replace(' uma ', ' ')
        texto = texto.replace(' umas ', ' ')
        return texto


    # Simplifica o texto de entrada para tornar a comparação entre as frases mais eficiente
    @staticmethod
    def limpar_texto(texto):
        texto = texto.lower()
        texto = Levenshtein.remover_acentos(texto)
        texto = Levenshtein.remover_caracteres_especiais(texto)
        texto = Levenshtein.remover_sinais_pontuacao(texto)
        texto = Levenshtein.remover_palavras_simples(texto)
        return texto


    # Método principal que compara as frases entre dois textos e retorna o percentual de similaridade entre eles
    @staticmethod
    @benchmark(num_iters=10)
    def compara_textos(texto1, texto2):
        # Simplificação dos textos de entrada
        texto1 = Levenshtein.limpar_texto(texto1)
        texto2 = Levenshtein.limpar_texto(texto2)

        # Exibe o número de caracteres de cada texto após a simplificação
        #print('Tamanho do texto1: ', len(texto1))
        #print('Tamanho do texto2: ', len(texto2))
        #print('')

        # Separa os dois textos em listas com frases. Os sinais de ? e ! foram convertidos em .
        lista1 = texto1.split('. ')
        lista2 = texto2.split('. ')

        # Exibe a quantidade de frases de cada texto
        #print('Quantidade de frases do texto1: ', len(lista1))
        #print('Quantidade de frases do texto2: ', len(lista2))
        #print('')

        # Esta lista irá a armazenar a quantidade de palavras e o percentual de similaridade de cada frase do texto 1
        lista_similaridade = []

        # Loop que fará a comparação de cada frase do texto1
        for i in range(0, len(lista1)):
            d_max = 1000
            posicao_j = 0
            qt_palavras1 = 0
            qt_palavras2 = 0

            # Exibe cada frase do texto1 antes de compará-la às frases do texto2
            #print(lista1[i])

            # Loop que fará a comparação com cada frase do texto2
            for j in range(0, len(lista2)):

                # Para cada frase do texto2, calcula-se a distância de Levenshtein
                distancia, m, n = Levenshtein.levenshtein_palavra(lista1[i], lista2[j])

                # Se a distância de Levenshtein encontrada for menor que a distância máxima:
                # A frase do texto2 corrente possui uma similaridade melhor com a frase do texto1
                # Nesta situação, devemos guardar os valores encontrados
                if distancia < d_max:
                    d_max = distancia
                    posicao_j = j
                    qt_palavras1 = m
                    qt_palavras2 = n

            # Ao percorrer todas as frases do texto2, podemos identificar qual delas possui maior similaridade com o texto1
            # Calcula-se o percentual de similaridade entre as duas frases
            percent_similaridade = 0
            if qt_palavras1 > 0:
                percent_distancia = (d_max / qt_palavras1) * 100
                percent_similaridade = 100 - percent_distancia

            # Exibição da frase do texto2 que possui maior similaridade com o texto1
            #print('Frase com maior similaridade:')
            #print(lista2[posicao_j])

            # Exibição da menor distância de Levenshtein entre as duas frases do texto1 e texto2
            #print('Distância Mínima: ', d_max)

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
        #print('')

        # Exibe a lista de similaridades
        #print('Lista de similaridades: ', lista_similaridade)

        # Exibe a similaridade total entre os texto1 e texto2
        #print('Similaridade total entre os textos: ', similaridade)
        return similaridade

