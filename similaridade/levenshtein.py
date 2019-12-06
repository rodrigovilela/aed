# -*- coding: utf-8 -*-
import numpy as np
from benchmarkit import benchmark


class Levenshtein:

    """
    Algoritmo de similaridade - Levenshtein
    """

    # Calcula a distância de Leventheins comparando caracteres entre palavras
    @staticmethod
    def levenshtein_caractere(s1, s2):
        m = len(s1) + 1
        n = len(s2) + 1

        matriz = np.zeros((m, n))

        for i in range(0, m):
            matriz[i][0] = i

        for i in range(0, n):
            matriz[0][i] = i

        for i in range(1, m):
            for j in range(1, n):
                if s1[i - 1] == s2[j - 1]:
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
        print(matriz)
        distancia = (matriz[m - 1, n - 1])
        #print('Distância de Levenshtein: ', distancia)
        return distancia

    # Calcula a distância de Leventheins comparando palavras entre frases
    @staticmethod
    def levenshtein_palavra(l1, l2):
        # print('Lista 1: ', l1)
        # print('Lista 2: ', l2)
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
        max_palavras = max(m - 1, n - 1)
        similaridade = 1 - distancia / max_palavras
        #print('Tamanho texto1: ', m - 1)
        #print('Tamanho texto2: ', n - 1)
        #print('Distância de Levenshtein: ', distancia)
        #print('Similaridade: ', similaridade)
        return similaridade

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
        texto = texto.replace('<br>', '')
        texto = texto.replace(' a ', ' ')
        texto = texto.replace(' as ', ' ')
        texto = texto.replace(' e ', ' ')
        texto = texto.replace(' o ', ' ')
        texto = texto.replace(' os ', ' ')
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
        texto = Levenshtein.remover_sinais_pontuacao(texto)
        texto = Levenshtein.remover_palavras_simples(texto)
        texto = Levenshtein.remover_caracteres_especiais(texto)
        return texto

    # Método principal que compara as frases entre dois textos e retorna o percentual de similaridade entre eles
    @staticmethod
    @benchmark()
    def compara_textos(texto1, texto2):

        # Simplificação dos textos de entrada
        texto1 = Levenshtein.limpar_texto(texto1)
        texto2 = Levenshtein.limpar_texto(texto2)

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
            palavras1 = lista1[i].split()
            qt_palavras1 = len(palavras1)
            max_indice_levenshtein = 0
            posicao_j = 0

            # Exibe cada frase do texto1 antes de compará-la às frases do texto2
            #print(lista1[i])

            # Loop que fará a comparação com cada frase do texto2
            for j in range(0, len(lista2)):

                palavras2 = lista2[j].split()
                indice_levenshtein = Levenshtein.levenshtein_palavra(palavras1, palavras2)

                # Se o índice de Levenshtein encontrado for maior que índice máximo:
                # A frase do texto2 corrente possui uma similaridade melhor com a frase do texto1
                # Nesta situação, devemos guardar os valores encontrados
                if indice_levenshtein > max_indice_levenshtein:
                    max_indice_levenshtein = indice_levenshtein
                    posicao_j = j

            # Ao percorrer todas as frases do texto2, podemos identificar qual delas possui maior similaridade com o texto1
            # Calcula-se o percentual de similaridade entre as duas frases
            # percent_distancia = (d_max / qt_palavras) * 100
            percent_similaridade = max_indice_levenshtein * 100

            # Exibição da frase do texto2 que possui maior similaridade com o texto1
            #print('Frase com maior similaridade:')
            #print(lista2[posicao_j])

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

    # Método principal que compara os textos utilizando os algoritmos originais
    @benchmark()
    def compara_textos_original(texto1, texto2):
        palavras1 = texto1.split()
        palavras2 = texto2.split()
        indice_levenshtein = Levenshtein.levenshtein_palavra(palavras1, palavras2)
        print('Similaridade total entre os textos', indice_levenshtein * 100)
        return indice_levenshtein * 100
