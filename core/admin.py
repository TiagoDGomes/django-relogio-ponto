# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from core.models import RelogioPonto, Colaborador, Parametro, Matricula,\
    RegistroPonto
from django.utils.translation import ugettext_lazy as _
from core.forms import ParametroForm, ColaboradorForm, MatriculaInlineFormSet
from settings import STATIC_URL
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from core.sites import admin_site
from django.urls import reverse


class ParametroInline(admin.TabularInline):
    model = Parametro
    extra = 0
    max_num = 0
    form = ParametroForm
    can_delete = False

@admin.register(RelogioPonto)
class RelogioPontoAdmin(admin.ModelAdmin):
    inlines = [ParametroInline,]
    list_display = ['nome', 'tipo', 'ativo', ]
    
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
    formset = MatriculaInlineFormSet
    
    

class RegistroPontoInline(admin.TabularInline):
    model = RegistroPonto
    extra = 0
    readonly_fields = ['relogio', 'data_hora', ]
    fields = ['data_hora', 'relogio', 'exportado' ]
    can_delete = False
    fieldsets = []


def salvar_em_relogios(modeladmin, request, queryset):
    #queryset.update(parecer='Aprovado')
    for colaborador in queryset.all():
        colaborador.salvar_em_relogios()
salvar_em_relogios.short_description = "Salvar selecionados em todos os relógios"
 
        
@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    search_fields = ('nome', 'pis', 'matriculas__numero')
    inlines = [MatriculaInline, ]    
    list_display = ['nome', 'get_link_batidas','pis','verificar_digital','get_matriculas']
    form = ColaboradorForm
    fieldsets = [
                 ('Informações básicas', {'fields':['nome', 'pis','verificar_digital',]}) ,
                 ('Opções', {'fields': 
                             ['salvar_em_relogios', 'forcar_sobrescrita'] 
                            } 
                  ),
                    
                ]
    
    class Media:
        js = (
              STATIC_URL + 'js/colaborador_admin.js',              
              )
    
    actions = (salvar_em_relogios,)
    def get_actions(self, request):
        actions = super(ColaboradorAdmin, self).get_actions(request)
        del actions['delete_selected']
        
        return actions 
    
    def get_link_batidas(self, obj):
        return '<a href="{0}">Registros</a>'.format(reverse('batidas', args=(obj.id,)))
    get_link_batidas.allow_tags = True
    get_link_batidas.short_description = _('Batidas')
    

    def get_matriculas(self, obj):
        matriculas =  (str(x['numero']) for x in obj.matriculas.values('numero'))
        return "\n".join(matriculas)
    get_matriculas.allow_tags = True
    get_matriculas.short_description = _('matrículas')
    
    
    '''def save_related(self, request, form, formsets, change):
        admin.ModelAdmin.save_related(self, request, form, formsets, change)
        relogios_a_salvar = form.cleaned_data['salvar_em_relogios'].all()
        form.instance.salvar_em_relogios(relogios_a_salvar)
    '''    

admin_site.register(Colaborador, ColaboradorAdmin)
admin_site.register(RelogioPonto, RelogioPontoAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)




