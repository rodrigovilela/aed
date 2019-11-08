from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from hello.forms import BuscarNoticiaForm
from similaridade.kmp import KPM
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

            if noticia not in noticias_relacionadas and KPM.busca_kmp_primeira_ocorrencia(noticia.texto.lower(), trecho.valor, l_posicoes) >= 0:
                noticias_relacionadas.append(noticia)

    return render(request, "news.html", {"noticia": noticia_buscada, "relacionadas": noticias_relacionadas})


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
