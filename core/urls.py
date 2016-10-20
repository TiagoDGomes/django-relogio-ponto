# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
import core
from core import views
from django.contrib import admin


admin.site.site_header = _('Sistema de ponto eletrônico')
admin.site.index_title = admin.site.index_title 
admin.site.site_title = admin.site.index_title 

urlpatterns = [
    url(r'^$', views.index ) ,  
    url(r'^gerar_arquivo$', views.gerar_arquivo, name='gerar_arquivo' )  , 
    url(r'^syslogout$', views.site_logout, name='site_logout' )  , 
            
]
