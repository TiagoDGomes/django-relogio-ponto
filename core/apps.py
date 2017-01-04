# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig
from core.runner import update_afd



class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = _('Sistema de ponto eletrônico')
    
    def ready(self):
        update_afd.after_response()