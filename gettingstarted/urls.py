from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("buscar/", hello.views.buscar, name="buscar"),
    path("trechos/", hello.views.trechos, name="trechos"),
    path("similaridades/", hello.views.similaridades, name="similaridades"),
    path("news/<int:id>", hello.views.news, name="news"),
    path("news-kmp/<int:id>", hello.views.news_kmp, name="news-kmp"),
    path("news-j/<int:id>", hello.views.news_jaccard, name="news-j"),
    path("news-leve/<int:id>", hello.views.news_levenshtein, name="news-leve"),
    path("news-cos/<int:id>", hello.views.news_cosine, name="news-cos"),
    path("news-grafico/<int:id>", hello.views.news_grafico),
    path("news-arvore/<int:id>", hello.views.news_arvore),
    path("admin/", admin.site.urls),
]
