# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from core import views
from django.contrib import admin


admin.site.site_header = _('Sistema de ponto eletrônico')
admin.site.index_title = admin.site.index_title 
admin.site.site_title = admin.site.index_title 

urlpatterns = [
    url(r'^$', views.index, name='index' ) ,  
    url(r'^gerar_arquivo$', views.gerar_arquivo, name='gerar_arquivo' )  , 
    url(r'^importar_arquivo_csv$', views.importar_arquivo_csv, name='importar_arquivo_csv' )  , 
    url(r'^salvar_colaborador$', views.salvar_colaboradores, name='salvar_colaboradores' )  , 
    url(r'^colaboradores$', views.colaboradores, name='colaboradores' )  , 
    url(r'^syslogout$', views.site_logout, name='site_logout' )  , 
            
]
