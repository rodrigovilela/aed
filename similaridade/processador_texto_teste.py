import unittest

from similaridade.processador_texto import ProcessadorTexto


class ProcessadorTextoTeste(unittest.TestCase):
    def test_extrair_trechos(self):
        texto = "Texto contendo mais de um trecho. " \
                "Cada Trecho será separado por ponto final. Mas existem outros terminadores de frase? " \
                "Sim, existem! Todos serão convertidos."
        trechos = ProcessadorTexto.extrair_trechos(texto)
        print(trechos)

        self.assertEqual(5, len(trechos))


    def test_gerar_hash(self):
        texto = "Texto contendo mais de um trecho. " \
                "Cada Trecho será separado por ponto final. Mas existem outros terminadores de frase? " \
                "Sim, existem! Todos serão convertidos."

        trechos = ProcessadorTexto.extrair_trechos(texto)
        hashs = []

        for trecho in trechos:
            hashs.append(ProcessadorTexto.gerar_hash(trecho))

        print(hashs)

        for trecho in trechos:
            self.assertIn(ProcessadorTexto.gerar_hash(trecho), hashs)

if __name__ == '__main__':
    unittest.main()
