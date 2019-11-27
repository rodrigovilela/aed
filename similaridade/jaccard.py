# -*- coding: utf-8 -*-
from benchmarkit import benchmark

from similaridade.processador_texto import ProcessadorTexto


class Jaccard:

    """
    Algoritmo de similaridade - Jaccard
    """
    @staticmethod
    @benchmark(num_iters=10)
    def similaridade_jaccard(t1, t2):
        trechos1 = ProcessadorTexto.extrair_trechos(t1)
        trechos2 = ProcessadorTexto.extrair_trechos(t2)
        match = 0
        for trecho1 in trechos1:
            for trecho2 in trechos2:
                if Jaccard.similaridade_trecho_jaccard(trecho1, trecho2) >= 0.5:
                    match = match + 1
                    break
        return match/len(trechos1)*100

    #
    @staticmethod
    def similaridade_trecho_jaccard(a, b):
        a = a.split()
        b = b.split()
        union = list(set(a + b))
        intersection = list(set(a) - (set(a) - set(b)))
        return float(len(intersection)) / len(union)

