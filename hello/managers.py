from django.db import models

class TrechoQuerySet(models.QuerySet):
    """
    Queries úteis ao modelo Trecho.
    """
    def buscar(self, valor=None, tipo=None):
        query = self
        if valor:
            query = query.filter(valor=valor)
        if tipo:
            query = query.filter(tipo=tipo)

        return query
