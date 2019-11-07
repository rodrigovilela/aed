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
    path("news/<int:id>", hello.views.news, name="news"),
    path("admin/", admin.site.urls),
]
