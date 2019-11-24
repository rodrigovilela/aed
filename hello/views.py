from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from hello.forms import BuscarNoticiaForm
from similaridade.bm import BoyerMoore
from similaridade.kmp import KPM
from similaridade.levenshtein import Levenshtein
from similaridade.tfidf import tfidf

from similaridade.cosine import cosine
from .models import TipoTrecho
from .models import Noticia
from .models import Trecho

from similaridade.processador_texto import ProcessadorTexto


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
    noticias = Noticia.objects.filter(trechos__in=noticia.trechos.all())\
        .exclude(id=noticia.id)\
        .distinct()\
        .order_by('-publicacao')

    return render(request, "news.html", {"noticia": noticia, "relacionadas": noticias})


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
    noticias = Noticia.objects.all().exclude(id=noticia_buscada.id)
    noticias_relacionadas = []
    for trecho in noticia_buscada.trechos.all().filter(tipo=TipoTrecho.TEXTO_NORMAL):

        for noticia in noticias:

            for trechoNoticia in noticia.trechos.all():

                if noticia not in noticias_relacionadas and \
                        similaridade_jaccard(trecho.valor, trechoNoticia.valor) >= 0.7:
                    noticias_relacionadas.append(noticia)

    return render(request, "news.html", {"noticia": noticia_buscada, "relacionadas": noticias_relacionadas})


def news_levenshtein(request, id):
    print('LEVE(', id, '): ')

    noticia_buscada = Noticia.objects.get(id=id)
    noticias = Noticia.objects.all().exclude(id=noticia_buscada.id)
    noticias_relacionadas = []

    for noticia in noticias:
        percentual = Levenshtein.compara_textos(noticia_buscada.texto, noticia.texto)
        print('Percentual(', noticia.id, '): ', percentual)
        if percentual[0] > 0:
            noticia.percentual = percentual[0]
            noticias_relacionadas.append(noticia)

    return render(request, "news-leve.html", {"noticia": noticia_buscada, "relacionadas": noticias_relacionadas})

def news_cosine(request, id):
    noticia_buscada = Noticia.objects.get(id=id)    
    noticias = [noticia for noticia in Noticia.objects.all().filter(veiculo='wikipedia')[:10]]
    
    vdocs = tfidf(noticias, True)
    tfidf_docs = vdocs.get_all_tf_idf()
    
    noticias_relacionadas = []
    for noticia in noticias:        
        tfidf_nb = [tfidf for word, tfidf in tfidf_docs[noticia_buscada.id].items()]
        tfidf_n = [tfidf for word, tfidf in tfidf_docs[noticia.id].items()]
        angle = cosine.similarity(tfidf_nb, tfidf_n)
        if (angle >= 0.3):
            noticias_relacionadas.append(noticia)
    
    return render(request, "news-cos.html", {"noticia": noticias, "relacionadas": noticias_relacionadas})


# --------------------------------------- AUXILIARES ---------------------------------------


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


def similaridade_jaccard(a, b):
    a = a.split()
    b = a.split()
    union = list(set(a + b))
    intersection = list(set(a) - (set(a) - set(b)))
    return float(len(intersection)) / len(union)
