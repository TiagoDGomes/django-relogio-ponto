from django.conf.urls import url
import core
from core import views
urlpatterns = [
    url(r'^$', views.index ) ,  
    url(r'^gerar_arquivo$', views.gerar_arquivo, name='gerar_arquivo' )  , 
            
]