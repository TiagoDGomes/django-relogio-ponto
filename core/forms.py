# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django import forms
from django.forms import widgets
from core.models import Colaborador, Matricula, RelogioPonto
from django.forms.widgets import Textarea
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from pyRelogioPonto.relogioponto.base import RelogioPontoException
from core import models
from pyRelogioPonto import relogioponto
import time
from brazilnum.pis import validate_pis
from django.core.exceptions import ValidationError
from core.util import somente_numeros
from urllib2 import HTTPError
from _warnings import warn


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput())
    

class GerarArquivoForm(forms.Form):
    inicio = forms.DateField()
    fim = forms.DateField()
    formato = forms.ChoiceField(choices=[('default',_('Formato padrão'))], label='Formato')
    @property
    def nome_arquivo(self):
        return "{0}-{1}".format( self.cleaned_data['inicio'].strftime('%d%m%Y'), self.cleaned_data['fim'].strftime('%d%m%Y'))


class ExportarParaRelogioForm(forms.Form):
    relogio = forms.ModelChoiceField(RelogioPonto.objects)
    
    def exportar(self, *args, **kwargs):
        relogio_banco =  self.cleaned_data['relogio']
        relogio_rep = relogio_banco.get_rep()
        relogio_rep.conectar()
        salvos = []
        erros = []
        for colaborador in models.Colaborador.objects.all():
            colaborador_rep = relogioponto.base.Colaborador(relogio_rep)
            colaborador_rep.nome = colaborador.nome
            colaborador_rep.pis = colaborador.pis
            colaborador_rep.matriculas = (m['numero'] for m in colaborador.matriculas.values('numero') )            
            try:
                self._salvar_em_rep(colaborador_rep) 
                salvos.append(colaborador)
            except RelogioPontoException as e:
                erros.append("{0} - {1}".format(colaborador, e.message))
            except HTTPError as httperr:
                warn(httperr.message)
                time.sleep(1)                
                try:
                    relogio_rep.conectar()
                    self._salvar_em_rep(colaborador_rep) 
                    salvos.append(colaborador)
                except Exception as ex:
                    erros.append("{0} - {1}".format(colaborador, ex.message))
        return salvos, erros  
              
    def _salvar_em_rep(self, colaborador_rep):                    
        try:
            colaborador_rep.save()                
        except RelogioPontoException as e:
            if not 'cadastrado para outro' in e.message:                    
                raise e     


class ColaboradorForm(forms.ModelForm):
    matriculas = forms.CharField(widget=Textarea(attrs={'rows':1, 'cols':6,}), required=False)
    
    class Meta:
        model = Colaborador
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ColaboradorForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'] is not None:
            colaborador = kwargs['instance']
            self.initial['matriculas'] = "\n".join ( str(m.numero) for m in colaborador.matriculas.all() ) 
 
    def save(self, *args, **kwargs):
        s = super(ColaboradorForm, self).save(*args, **kwargs)
        matriculas_post = self.cleaned_data['matriculas'].split('\n')        

        self.instance.matriculas.all().delete()
        self.instance.save()
        for numero_a_salvar in matriculas_post:
            if numero_a_salvar:
                matricula = Matricula()
                matricula.numero = somente_numeros(numero_a_salvar)
                matricula.colaborador = self.instance
                #matricula.colaborador.save()
               
                matricula.save()
        return s     
    
    def clean_pis(self, *args, **kwargs):
        pis = (somente_numeros(self.cleaned_data['pis'])) 
        valido = validate_pis(pis)               
        if not valido:            
            raise forms.ValidationError ("PIS inválido")
        else:    
            return int(pis)
        
    
    
                
ColaboradorFormSet = modelformset_factory(Colaborador, 
                                         form=ColaboradorForm, 
                                         extra=1, 
                                         fields=('__all__')) 
