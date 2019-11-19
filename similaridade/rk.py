class RabinKarp:

    """
    Algoritmo de Busca - Rabin Karp
    Objetivo: Comparar os caracteres de dois textos e verificar se existe String Matching
    Entrada:
    Texto: Texto para realizar a busca
    Padrão: String de busca
    Saída:
    """

    tabela_asc = {}


    def cria_tabela_asc():
        for i in range(32, 127):
            tabela_asc[chr(i)] = i
        print(tabela_asc)


    def calcula_hash(s):
        tam = len(s)
        exp = 0
        base = 3
        valor_hash = 0

        for caractere in s:
            valor_asc = tabela_asc.get(caractere)
            calc = (base**exp)*valor_asc
            valor_hash = valor_hash + calc
            exp += 1
        return valor_hash


    def calcula_hash_caractere(c, exp):
        base = 3
        valor_asc = tabela_asc.get(c)
        hash_caractere = (base**exp)*valor_asc
        return hash_caractere


    def busca_rk_primeira_ocorrencia(padrao, texto, hash_padrao):
        base = 3
        tam = len(padrao)
        posicao = 0
        fim = posicao + tam

        sub_texto = texto[posicao:fim]
        hash_sub_texto = calcula_hash(sub_texto)

        if hash_padrao == hash_sub_texto:
            return posicao
        else:
            posicao += 1
            fim += 1

            while fim <= len(texto):
                anterior = texto[posicao-1]
                valor_anterior = tabela_asc.get(anterior)

                sub_texto = texto[posicao:fim]
                proximo = sub_texto[tam-1]
                hash_proximo = calcula_hash_caractere(proximo, tam-1)

                hash_sub_texto = int((hash_sub_texto - valor_anterior)/base) + hash_proximo

                if hash_padrao == hash_sub_texto:
                    return posicao
                else:
                    posicao += 1
                    fim += 1
        return -1


    def busca_rk_todas_ocorrencias(padrao, texto, hash_padrao):
        retorno = []
        base = 3
        tam = len(padrao)
        posicao = 0
        fim = posicao + tam

        sub_texto = texto[posicao:fim]
        hash_sub_texto = calcula_hash(sub_texto)

        if hash_padrao == hash_sub_texto:
            retorno.append(posicao)
        else:
            posicao += 1
            fim += 1

            while fim <= len(texto):
                anterior = texto[posicao-1]
                valor_anterior = tabela_asc.get(anterior)

                sub_texto = texto[posicao:fim]
                proximo = sub_texto[tam-1]
                hash_proximo = calcula_hash_caractere(proximo, tam-1)

                hash_sub_texto = int((hash_sub_texto - valor_anterior)/base) + hash_proximo

                if hash_padrao == hash_sub_texto:
                    retorno.append(posicao)
                else:
                    posicao += 1
                    fim += 1
        return retorno


    cria_tabela_asc()
    l_hash_padrao = calcula_hash(s_padrao)

    ocorrencia = busca_rk_primeira_ocorrencia(s_padrao, s_texto, l_hash_padrao)
    if ocorrencia == -1:
        print('Não existe ocorrência do padrão do texto')
    else:
        print(f'O padrão foi encontrado no texto na posição: {ocorrencia}')

    ocorrencias = busca_rk_todas_ocorrencias(s_padrao, s_texto, l_hash_padrao)
    if len(ocorrencias) == 0:
        print('Não existem ocorrências do padrão do texto')
    else:
        print(f'O padrão foi encontrado no texto nas posições: {ocorrencias}')