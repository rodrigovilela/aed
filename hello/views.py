import io
import os.path
import pandas as pd
from benchmarkit import benchmark
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from hello.forms import BuscarNoticiaForm
from similaridade.bm import BoyerMoore
from similaridade.cosine import cosine
from similaridade.jaccard import Jaccard
from similaridade.kmp import KPM
from similaridade.levenshtein import Levenshtein
from similaridade.processador_texto import ProcessadorTexto
from similaridade.tfidf import tfidf, tfidfall, data_persistence

from .models import Noticia, TipoAlgoritmo, Similaridade
from .models import TipoTrecho
from .models import Trecho


def index(request):
    return render(request, 'index.html', {'noticias': buscar_noticias(None)})


def buscar(request):
    # if this is a POST request we need to process the form data
    termo = ''
    noticias = []
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BuscarNoticiaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            termo = form.cleaned_data['termo']
            noticias = buscar_noticias(termo)

    # if a GET (or any other method) we'll create a blank form
    else:
        noticias = buscar_noticias(None)
        form = BuscarNoticiaForm()

    return render(request, 'index.html', {'form': form, 'noticias': noticias, 'termo': termo})


def news(request, id):

    noticia = Noticia.objects.get(id=id)
    noticia.noticias_similares = recuperar_similares(noticia)

    return render(request, "news.html", {"noticia": noticia})


def trechos(request):

    noticias = Noticia.objects.all()

    for noticia in noticias:
        trechos_texto = ProcessadorTexto.extrair_trechos(noticia.texto)
        for trechoTexto in trechos_texto:
            trecho_tipo_texto = buscar_ou_criar_trecho(trechoTexto, TipoTrecho.TEXTO_NORMAL)
            trecho_tipo_hash = buscar_ou_criar_trecho(ProcessadorTexto.gerar_hash(trechoTexto), TipoTrecho.HASH_12)
            adicionar_trecho(noticia, trecho_tipo_texto)
            adicionar_trecho(noticia, trecho_tipo_hash)
        noticia.save()

    return news(request, noticias[0].id)


def similaridades(request):

    noticias = Noticia.objects.filter(id__gte=4900)

    ###
    path = 'C:/Users/Rodrigo/PycharmProjects/aed/noticias.txt'
    if not os.path.isfile(path):
        print("Construindo TDIDF para:", len(noticias))
        tfidf_write(noticias, True, path, True)

    tfidf_docs = tfidf_load(path)
    ###

    for noticia in noticias:
        print("Prcessando:", noticia.id)
        similares = Noticia.objects.filter(id__gte=4900).exclude(id=noticia.id)

        for similar in similares:

            percentualLeve = Levenshtein.compara_textos(noticia.texto, similar.texto)
            indiceJaccard = Jaccard.similaridade_jaccard(noticia.texto, similar.texto)
            indiceCosine = similaridade_cosine(noticia, similar, tfidf_docs)

            adicionar_similaridade(noticia, similar, TipoAlgoritmo.Levenshtein, percentualLeve[0])
            adicionar_similaridade(noticia, similar, TipoAlgoritmo.Jaccard, indiceJaccard[0])
            adicionar_similaridade(noticia, similar, TipoAlgoritmo.Cosine, indiceCosine[0])

        noticia.save()

    return news(request, noticias[0].id)

def news_kmp(request, id):

    noticia_buscada = Noticia.objects.get(id=id)
    noticias = Noticia.objects.all().exclude(id=noticia_buscada.id)
    noticias_relacionadas = []
    for trecho in noticia_buscada.trechos.all().filter(tipo=TipoTrecho.TEXTO_NORMAL):

        # Calcula a matriz de prefixos do padrão (texto de busca)
        l_posicoes = KPM.calcula_prefixo(trecho.valor)

        for noticia in noticias:

            if noticia not in noticias_relacionadas and KPM.busca_kmp_primeira_ocorrencia(
                    noticia.texto.lower(), trecho.valor, l_posicoes) >= 0:
                noticias_relacionadas.append(noticia)

    return render(request, "news.html", {"noticia": noticia_buscada, "relacionadas": noticias_relacionadas})

def news_bm(request, id):

    noticia_buscada = Noticia.objects.get(id=id)
    noticias = Noticia.objects.all().exclude(id=noticia_buscada.id)
    noticias_relacionadas = []
    for trecho in noticia_buscada.trechos.all().filter(tipo=TipoTrecho.TEXTO_NORMAL):

        # Calcula a tabela de saltos
        tabela = BoyerMoore.calcula_tabela_saltos(trecho.valor)

        for noticia in noticias:
            if noticia not in noticias_relacionadas and BoyerMoore.busca_bm_primeira_ocorrencia(
                    trecho.valor, noticia.texto.lower(), tabela) >= 0:
                noticias_relacionadas.append(noticia)

    return render(request, "news.html", {"noticia": noticia_buscada, "relacionadas": noticias_relacionadas})


def news_jaccard(request, id):

    noticia_buscada = Noticia.objects.get(id=id)
    noticias = Noticia.objects.all().exclude(id=noticia_buscada.id)[:500]
    noticias_relacionadas = []

    for noticia in noticias:
        percentual = Jaccard.similaridade_jaccard(noticia_buscada.texto, noticia.texto)
        #percentual = Jaccard.similaridade_jaccard("Minha bicicleta está com o pneu furado. Não quero arrumar.", "Não me pergunte. Minha bicicleta estragou o pneu. Vou consertar amanhã.")
        if noticia not in noticias_relacionadas and percentual[0] > 12:
            noticia.percentual = percentual[0]
            noticias_relacionadas.append(noticia)

    return render(request, "news-similaridade.html", {"noticia": noticia_buscada, "relacionadas": noticias_relacionadas, "similaridade": "-j"})


def news_levenshtein(request, id):
    noticia_buscada = Noticia.objects.get(id=id)
    noticias = Noticia.objects.all().exclude(id=noticia_buscada.id)[:500]
    noticias_relacionadas = []

    for noticia in noticias:
        percentual = Levenshtein.compara_textos(noticia_buscada.texto, noticia.texto)
        #print('Percentual(', noticia.id, '): ', percentual)
        if percentual[0] > 12:
            noticia.percentual = percentual[0]
            noticias_relacionadas.append(noticia)

    return render(request, "news-similaridade.html", {"noticia": noticia_buscada, "relacionadas": noticias_relacionadas, "tipo-similaridade": "-leve"})


def news_cosine(request, id):
    trecho = True
    noticia_buscada = Noticia.objects.get(id=id)

    noticias_relacionadas = []

    if trecho is True:
        noticias = [noticia for noticia in Noticia.objects.all().filter(veiculo='previdencia')[:100]]

        # Apenas para teste
        noticias.append(noticia_buscada)

        path = 'C:/Users/Rodrigo/PycharmProjects/aed/noticias.txt'

        if not os.path.isfile(path):
            tfidf_write(noticias, True, path, True)

        tfidf_docs = tfidf_load(path)

        lista_similaridade_trechos = list()
        lista_similaridade = list()

        for noticia in noticias:

            # Compara os trechos
            if (noticia.id != noticia_buscada.id):
                for id_noticia_nb, tfidf_trechos_nb in tfidf_docs[noticia_buscada.id].items():
                    for id_noticia_n, tfidf_trechos_n in tfidf_docs[noticia.id].items():
                        angle = cosine.similarity_as_dict(tfidf_trechos_nb[0], tfidf_trechos_n[0])
                        lista_similaridade_trechos.append([tfidf_trechos_nb[1], tfidf_trechos_n[1], angle])
                lista_similaridade.append((noticia.id, lista_similaridade_trechos))

        # Calculo de similaridade
        for id_noticia_n, lista_similaridade_trechos in lista_similaridade:

            peso = lista_similaridade_trechos[0][0]
            soma = 0

            for similaridade_trecho in lista_similaridade_trechos:
                peso = peso + similaridade_trecho[1]
                soma = soma + similaridade_trecho[0] * similaridade_trecho[2]

            similaridade = 0
            if peso > 0 and soma > 0:
                similaridade = soma / peso

            if (similaridade > 0.7):
                noticias_relacionadas.append(Noticia.objects.get(id=id_noticia_n))

    else:
        noticias = [noticia for noticia in Noticia.objects.all().filter(veiculo='previdencia')[:2]]
        # Apenas para teste
        noticias.append(noticia_buscada)

        noticias_trechos = converter_trechos(noticias)
        _tfidf = tfidf(noticias_trechos, True, trecho, '')
        tfidf_docs = _tfidf.get_all_tf_idf()

        for noticia in noticias:
            tfidf_nb = [tfidf for word, tfidf in tfidf_docs[noticia_buscada.id].items()]
            tfidf_n = [tfidf for word, tfidf in tfidf_docs[noticia.id].items()]
            angle = cosine.similarity(tfidf_nb, tfidf_n)
            if (angle >= 0.3):
                noticias_relacionadas.append(noticia)

    return render(request, "news-cos.html", {"noticia": noticia, "relacionadas": noticias_relacionadas})


def news_grafico(request, id):
    noticia_buscada = Noticia.objects.get(id=id)
    #noticias = Noticia.objects.all().exclude(id=noticia_buscada.id)[:50]
    noticias = Noticia.objects.filter(id__gte=5000, id__lte=5014).exclude(id=noticia_buscada.id)

    ### cosine
    # Apenas para teste
    #noticias.append(noticia_buscada)

    path_o = 'C:/Users/Rodrigo/PycharmProjects/aed/noticias_o.txt'
    path = 'C:/Users/Rodrigo/PycharmProjects/aed/noticias.txt'

    if not os.path.isfile(path_o):
        noticias_todas = []
        noticias_todas.extend(noticias)
        if noticia_buscada not in noticias_todas:
            noticias_todas.append(noticia_buscada)
        tfidf_write(noticias_todas, False, path_o, False)


    if not os.path.isfile(path):
        noticias_todas = []
        noticias_todas.extend(noticias)
        if noticia_buscada not in noticias_todas:
            noticias_todas.append(noticia_buscada)
        tfidf_write(noticias_todas, True, path, True)



    tfidf_docs_o = tfidf_load(path_o)
    tfidf_docs = tfidf_load(path)
    ###

    plo = []  #percentual similaridade levenshtein original
    pjo = []  #percentual similaridade jaccar original
    pco = []  # percentual similaridade cosine original
    pl = []  #percentual similaridade levenshtein
    pj = []  #percentual similaridade jaccar
    pc = []  #percentual similaridade cosine
    tamanhos = []
    indices = []
    elemento = 0

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    for noticia in noticias:
        print("Prcessando:", noticia.id)


        percentualLeveO = Levenshtein.compara_textos_original(noticia_buscada.texto, noticia.texto)
        indiceJaccardO = Jaccard.similaridade_jaccard_original(noticia_buscada.texto, noticia.texto)
        indiceCosineO = similaridade_cosine_original(noticia_buscada, noticia, tfidf_docs_o)
        percentualLeve = Levenshtein.compara_textos(noticia_buscada.texto, noticia.texto)
        indiceJaccard = Jaccard.similaridade_jaccard(noticia_buscada.texto, noticia.texto)
        indiceCosine = similaridade_cosine(noticia_buscada, noticia, tfidf_docs)

        plo.append(percentualLeveO[0])
        pjo.append(indiceJaccardO[0])
        pco.append(indiceCosineO[0])
        pl.append(percentualLeve[0])
        pj.append(indiceJaccard[0])
        pc.append(indiceCosine[0])

        #print("Levenshtein:", noticia.id, percentualLeve[0])

        tamanhos.append(len(noticia.texto))
        indices.append(elemento)
        elemento = elemento + 1

    df = pd.DataFrame({'Levenshtein': plo, 'Jaccard': pjo, 'Cosine': pco, 'Levenshtein Adaptado': pl, 'Jaccard Adaptado': pj, 'Cosine Adaptado': pc}, index=tamanhos)
    #df = pd.DataFrame( {'Levenshtein': plo, 'Jaccard': pjo, 'Cosine': pco}, index=tamanhos)
    #df = pd.DataFrame({'Levenshtein Adaptado': pl, 'Jaccard Adaptado': pj, 'Cosine Adaptado': pc}, index=tamanhos)

    df.sort_index(inplace=True)
    print(df)
    ax.set(xlabel='tamanho texto (caracteres)', ylabel='% de similaridade', title='Algoritmos de similaridade: Tamanho X Percentual de similaridade')

    ax.plot(df)
    ax.legend(['Levenshtein', 'Jaccard', 'Cosine', 'Levenshtein Adaptado', 'Jaccard Adaptado', 'Cosine Adaptado'])
    #ax.legend(['Levenshtein', 'Jaccard', 'Cosine'])
    #ax.legend(['Levenshtein Adaptado', 'Jaccard Adaptado', 'Cosine Adaptado'])

    buf = io.BytesIO()
    canvas.print_png(buf)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    fig.clear()
    response['Content-Length'] = str(len(response.content))
    return response


def news_arvore(request, id):
    noticia = Noticia.objects.get(id=id)
    noticia.noticias_similares = recuperar_similares(noticia)

    for similar in noticia.noticias_similares:
        print('filhos de ', similar.noticia_similar.id)
        similar.noticia_similar.noticias_similares = recuperar_similares(similar.noticia_similar)
        print(similar.noticia_similar.noticias_similares)

    return render(request, "arvore.html", {"noticia": noticia})


# --------------------------------------- AUXILIARES ---------------------------------------
@benchmark()
def similaridade_cosine_original(noticia_buscada, noticia, tfidf_docs):
    tfidf_nb = [tfidf for word, tfidf in tfidf_docs[noticia_buscada.id].items()]
    tfidf_n = [tfidf for word, tfidf in tfidf_docs[noticia.id].items()]
    similaridade = cosine.similarity(tfidf_nb, tfidf_n)

    return 100 * similaridade

@benchmark()
def similaridade_cosine(noticia_buscada, noticia, tfidf_docs):
    lista_similaridade_trechos = list()
    lista_similaridade = list()

    # Compara os trechos
    for id_noticia_nb, tfidf_trechos_nb in tfidf_docs[noticia_buscada.id].items():

        trecho_mais_similar = [0, 0, 0]

        for id_noticia_n, tfidf_trechos_n in tfidf_docs[noticia.id].items():
            angle = cosine.similarity_as_dict(tfidf_trechos_nb[0], tfidf_trechos_n[0])
            if trecho_mais_similar[2] < angle:
                trecho_mais_similar = [tfidf_trechos_nb[1], tfidf_trechos_n[1], angle]

        lista_similaridade_trechos.append(trecho_mais_similar)
    lista_similaridade.append((noticia.id, lista_similaridade_trechos))

    # Calculo de similaridade
    similaridade = 0
    for id_noticia_n, lista_similaridade_trechos in lista_similaridade:

        peso = 0
        soma = 0

        for similaridade_trecho in lista_similaridade_trechos:
            peso = peso + similaridade_trecho[0]
            soma = soma + similaridade_trecho[0] * similaridade_trecho[2]

        similaridade = 0
        if peso > 0 and soma > 0:
            similaridade = soma / peso

    return 100 * similaridade


def adicionar_similaridade(noticia, similar, tipo, percentual):
    if percentual > 15:
        similaridade = Similaridade(percentual=round(percentual, 2), tipo=tipo, similar=similar.id)
        similaridade.save()
        noticia.similares.add(similaridade)


def recuperar_similares(noticia):
    similares = []
    for similaridade in noticia.similares.all():
        if similaridade.tipo == TipoAlgoritmo.Levenshtein:
            similaridade.noticia_similar = Noticia.objects.get(id=similaridade.similar)
            similares.append(similaridade)
    return similares


def buscar_ou_criar_trecho(valor, tipo):
    trecho = Trecho.objects.filter(valor=valor, tipo=tipo).first()
    if not trecho:
        trecho = Trecho(valor=valor, tipo=tipo)
        trecho.save()
    return trecho


def adicionar_trecho(noticia, trecho):
    if trecho not in noticia.trechos.all():
        noticia.trechos.add(trecho)


def buscar_noticias(termo):
    if termo:
        noticias = Noticia.objects.filter(Q(titulo__icontains=termo) | Q(texto__icontains=termo)) \
                .order_by('-publicacao')
    else:
        noticias = Noticia.objects.all().order_by('-publicacao')[:10]
    return noticias


def recuperar_similares_por_trecho(noticia):
    return Noticia.objects.filter(trechos__in=noticia.trechos.all()) \
        .exclude(id=noticia.id) \
        .distinct() \
        .order_by('-publicacao')

def converter_trechos(noticias):

    _noticias = list()

    for noticia in noticias:
        trechos_texto = ProcessadorTexto.extrair_trechos(noticia.texto)
        for trechoTexto in trechos_texto:
            trecho_tipo_texto = buscar_ou_criar_trecho(trechoTexto, TipoTrecho.TEXTO_NORMAL)
            adicionar_trecho(noticia, trecho_tipo_texto)
        noticia.save()
        _noticias.append(noticia)

    return _noticias


def tfidf_write(noticias, trecho, path, stopwords):
    if trecho is True:
        noticias_trechos = converter_trechos(noticias)
        tfidf_noticia_trecho = [tfidf(nt.trechos.all().filter(tipo=TipoTrecho.TEXTO_NORMAL), stopwords, trecho, nt.id)
                                for nt in noticias_trechos]
        _tfidfall = tfidfall(tfidf_noticia_trecho, stopwords)

        tfidf_docs = {}
        for elem in tfidf_noticia_trecho:
            tfidf_docs[elem.id_noticia] = _tfidfall.get_tf_idf(elem)
    else:
        _tfidf = tfidf(noticias, stopwords, trecho, '')
        tfidf_docs = _tfidf.get_all_tf_idf()

    data_persistence.write(tfidf_docs, path)


def tfidf_load(path):
    return data_persistence.load(path)
