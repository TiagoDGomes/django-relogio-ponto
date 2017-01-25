# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig



class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = _('Sistema de ponto eletrônico')
    
    def ready(self):        
        pass
        