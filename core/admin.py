# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from core.models import RelogioPonto, Colaborador, Parametro, Matricula,\
    RegistroPonto
from django.utils.translation import ugettext_lazy as _
from core.forms import ParametroForm, ColaboradorForm
from settings import STATIC_URL
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from core.sites import admin_site



class ParametroInline(admin.TabularInline):
    model = Parametro
    extra = 0
    max_num = 0
    form = ParametroForm
    can_delete = False

@admin.register(RelogioPonto)
class RelogioPontoAdmin(admin.ModelAdmin):
    inlines = [ParametroInline,]
    list_display = ['nome', 'tipo',]
    
    class Media:
        js = (
              STATIC_URL + 'js/relogio_ponto_admin.js',              
              )
              
    def get_inline_instances(self, request, obj=None):
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        else:
            return []
        
    def add_view(self, request,  form_url='', extra_context=None):
        extra_context = extra_context or {}        
        extra_context['show_save'] = False                
        return super(RelogioPontoAdmin, self).add_view(request, form_url, extra_context=extra_context)
    

class MatriculaInline(admin.TabularInline):
    model = Matricula
    extra = 1
    

class RegistroPontoInline(admin.TabularInline):
    model = RegistroPonto
    extra = 0
    readonly_fields = ['relogio', 'data_hora', ]
    fields = ['data_hora', 'relogio', 'exportado' ]
    can_delete = False
    fieldsets = []
    
        
@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    inlines = [MatriculaInline, ]    
    list_display = ['nome', 'pis','verificar_digital','get_matriculas']
    form = ColaboradorForm
    fieldsets = [
                 ('Informações básicas', {'fields':['nome', 'pis','verificar_digital',]}) ,
                 
                    
                ]
    
    class Media:
        js = (
              STATIC_URL + 'js/colaborador_admin.js',              
              )
    
    
    def get_matriculas(self, obj):
        matriculas =  (str(x['numero']) for x in obj.matriculas.values('numero'))
        return "\n".join(matriculas)
    get_matriculas.allow_tags = True
    get_matriculas.short_description = _('matrículas')
    


admin_site.register(Colaborador, ColaboradorAdmin)
admin_site.register(RelogioPonto, RelogioPontoAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)




