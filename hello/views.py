from django.shortcuts import render
from django.http import HttpResponse

from .models import TipoTrecho
from .models import Noticia
from .models import Trecho

from similaridade.processador_texto import ProcessadorTexto

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def news(request, id):

    noticia = Noticia.objects.get(id=id)
    trechosTexto = ProcessadorTexto.extrair_trechos(noticia.texto)

    for trechoTexto in trechosTexto:
        trechoTipoTexto = buscarOuCriarTrecho(trechoTexto, TipoTrecho.TEXTO_NORMAL)
        trechoTipoHash = buscarOuCriarTrecho(ProcessadorTexto.gerar_hash(trechoTexto), TipoTrecho.HASH_12)
        adicionarTrecho(noticia, trechoTipoTexto)
        adicionarTrecho(noticia, trechoTipoHash)
        noticia.save()

    noticias = Noticia.objects.all()

    return render(request, "news.html", {"noticia": noticia, "relacionadas": noticias})


def buscarOuCriarTrecho(valor, tipo):
    trecho = Trecho.objects.filter(valor=valor, tipo=tipo).first()
    if not trecho:
        trecho = Trecho(valor=valor, tipo=tipo)
        trecho.save()
    return trecho

def adicionarTrecho(noticia, trecho):
    if trecho not in noticia.trechos.all():
        noticia.trechos.add(trecho)
