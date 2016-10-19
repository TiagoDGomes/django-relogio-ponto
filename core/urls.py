from django.conf.urls import url
import core
from core import views
urlpatterns = [
    url(r'^', views.index )           
]