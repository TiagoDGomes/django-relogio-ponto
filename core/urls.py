# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from core import views
from django.contrib import admin
from core.sites import SitePlus

#admin.site = SitePlus()
admin.site.site_title = _('Sistema de controle de relógio de ponto')
admin.site.index_title = _('Sistema de controle de relógio de ponto')
admin.site.site_header = _('Sistema de controle de relógio de ponto')
admin.site.site_url = None

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'


urlpatterns = [
    url(r'^gerar_arquivo$', views.gerar_arquivo, name='gerar_arquivo' )  , 
    url(r'^recuperar_batidas$', views.recuperar_batidas, name='recuperar_batidas' )  , 
    url(r'^importar_arquivo_csv$', views.importar_arquivo_csv, name='importar_arquivo_csv' )  , 
    url(r'^exportar_para_relogio$', views.exportar_para_relogio, name='exportar_para_relogio' )  , 
    url(r'^salvar_colaborador$', views.salvar_colaboradores, name='salvar_colaboradores' )  , 
    url(r'^colaboradores$', views.colaboradores, name='colaboradores' )  , 
    url(r'^syslogout$', views.site_logout, name='site_logout' )  ,
    url(r'^$', views.index, name='index' ) ,  
    
]

