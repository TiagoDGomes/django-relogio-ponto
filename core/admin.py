# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from core.models import RelogioPonto, Colaborador, Parametro, Matricula

class ParametroInline(admin.StackedInline):
    model = Parametro
    extra = 0
    max_num = 0
    

@admin.register(RelogioPonto)
class RelogioPontoAdmin(admin.ModelAdmin):
    inlines = [ParametroInline,]
    list_display = ['nome', 'tipo',]
    
    def get_inline_instances(self, request, obj=None):
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        else:
            return []
        
    def add_view(self, request,  form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False             
        return super(RelogioPontoAdmin, self).add_view(request, form_url, extra_context=extra_context)
    

class MatriculaInline(admin.StackedInline):
    model = Matricula
    extra = 1
        
@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    inlines = [MatriculaInline,]
