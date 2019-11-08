class KPM():
    """
    Algoritmo de Busca - Knuth Morris Pratt
    Objetivo: Comparar os caracteres de dois textos e verificar se existe String Matching
    Entrada:
    Texto: Texto para realizar a busca
    Padrão: String de busca
    Saída:
    """

    # Retorna a matriz de prefixos com os valores para cada caractere do padrão
    @staticmethod
    def calcula_prefixo(padrao):
        i = 1
        j = 0

        # Transforma a String em uma matriz m x 2, onde m é o tamanho da String padrão
        posicoes = []
        for char in padrao:
            posicoes.append([char, 0])

        while i < len(posicoes):
            if posicoes[i][0] != posicoes[j][0]:
                if j > 0:
                    j = posicoes[j-1][1]
                else:
                    posicoes[i][1] = j
                    i += 1
            else:
                j += 1
                posicoes[i][1] = j
                i += 1
        return posicoes


    # Encontra a primeira ocorrência do padrão em um texto e retorna a posição do String Matching no texto
    # Se não for encaontrada, retorna -1
    @staticmethod
    def busca_kmp_primeira_ocorrencia(texto, padrao, posicoes):

        i_padrao = 0

        for i_texto in range(len(texto)):
            while i_padrao > 0 and texto[i_texto] != padrao[i_padrao]:
                i_padrao = posicoes[i_padrao-1][1]
            if texto[i_texto] == padrao[i_padrao]:
                i_padrao += 1
                if i_padrao == len(padrao):
                    return i_texto - (i_padrao - 1)
        return -1


    # Encontra a todas as ocorrência da lista em um texto e retorna um vetor com uma lista de posição do String Matching
    # no texto. Se não for encontrada nenhuma ocorrência retorna uma lista vazia
    @staticmethod
    def busca_kmp_todas_ocorrencias(texto, padrao, posicoes):

        i_padrao = 0
        retorno = []

        for i_texto in range(len(texto)):
            while i_padrao > 0 and texto[i_texto] != padrao[i_padrao]:
                i_padrao = posicoes[i_padrao-1][1]
            if texto[i_texto] == padrao[i_padrao]:
                i_padrao += 1
                if i_padrao == len(padrao):
                    posicao = i_texto - (i_padrao - 1)
                    retorno.append(posicao)
                    i_padrao = 0
        return retorno