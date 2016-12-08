# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.utils.translation import ugettext_lazy as _
from core import views
from django.contrib import admin
from core.admin import admin_site


urlpatterns = [
    url(r'^ponto/$', views.index, name='index' ) ,  
    url(r'^ponto/gerar_arquivo$', views.gerar_arquivo, name='gerar_arquivo' )  , 
    url(r'^ponto/importar_arquivo_csv$', views.importar_arquivo_csv, name='importar_arquivo_csv' )  , 
    url(r'^ponto/exportar_para_relogio$', views.exportar_para_relogio, name='exportar_para_relogio' )  , 
    url(r'^ponto/salvar_colaborador$', views.salvar_colaboradores, name='salvar_colaboradores' )  , 
    url(r'^ponto/colaboradores$', views.colaboradores, name='colaboradores' )  , 
    url(r'^ponto/syslogout$', views.site_logout, name='site_logout' )  ,
    url(r'^ponto/sistema/', admin_site.urls, name="pagina_inicial"),      
]

