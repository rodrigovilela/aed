from django.db import models

from hello.managers import TrechoQuerySet

from enum import IntEnum


class TipoTrecho(IntEnum):
    TEXTO_NORMAL = 1
    HASH_12 = 2
    OUTRO = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Trecho(models.Model):
    valor = models.TextField()
    tipo = models.IntegerField(choices=TipoTrecho.choices(), default=TipoTrecho.TEXTO_NORMAL)

    objects = TrechoQuerySet.as_manager()

    def __str__(self):
        return self.valor

class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    texto = models.TextField()
    publicacao = models.DateField()
    veiculo = models.CharField(max_length=255)
    trechos = models.ManyToManyField(Trecho)

    def __str__(self):
        return self.titulo