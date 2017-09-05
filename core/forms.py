# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django import forms
from django.forms import widgets
from core.models import Colaborador, Matricula, RelogioPonto, RegistroPonto,\
    Parametro
from django.forms.widgets import Textarea
from django.forms.models import modelformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from pyRelogioPonto.relogioponto.base import RelogioPontoException
from core import models
from pyRelogioPonto import relogioponto
import time
from brazilnum.pis import validate_pis
from core.util import somente_numeros
from urllib2 import HTTPError
from _warnings import warn
from django.db.models import Q
from datetime import datetime
from pyRelogioPonto.relogioponto.base import Colaborador as ColaboradorREP
from django.core.exceptions import ValidationError
import django




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput())
    

class GerarArquivoForm(forms.Form):
    inicio = forms.DateField()
    fim = forms.DateField()
    formato = forms.ChoiceField(choices=[('default',_('Formato padrão')),
                                         ('rapido',_('Formato visualização rápida')),                                         
                                         ], label='Formato')
    
    @property
    def nome_arquivo(self):
        if self.cleaned_data['inicio'] == self.cleaned_data['fim']:
            return "{0}".format( self.cleaned_data['inicio'].strftime('%Y-%m-%d'))
        return "{0}.{1}".format( self.cleaned_data['inicio'].strftime('%Y-%m-%d'), self.cleaned_data['fim'].strftime('%Y-%m-%d'))
    
    def gerar(self):
        
        data_inicio = datetime.combine(self.cleaned_data['inicio'], datetime.min.time())        
        data_fim = datetime.combine(self.cleaned_data['fim'], datetime.max.time())
        
        registros = RegistroPonto.objects.filter(
                                                Q(data_hora__gte=data_inicio)&
                                                Q(data_hora__lte=data_fim)                                                  
                                                 ).order_by('data_hora')
        if self.cleaned_data['formato'] == 'rapido':
            formato = [('matricula', 5), 
                       ('datahora', "\t%d/%m/%y\t%H:%M"),                       
                      ]
        else:
            formato = [('matricula',15), 
                       ('datahora', "%d%m%y%H%M"),
                       ('personalizado','00100100'),
                      ]
        resultado = []
        for registro in registros:           
            resultado.append(registro.converter_em_texto(formato))
        return "\r\n".join(resultado)
    

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
            for m in colaborador.matriculas.values('numero'):
                colaborador_rep.matriculas.append(m['numero'])            
            try:
                self._salvar_em_rep(colaborador_rep) 
                salvos.append(colaborador)
            except HTTPError as httperr:
                warn(httperr.message)
                time.sleep(1)                
                try:
                    relogio_rep.conectar()
                    self._salvar_em_rep(colaborador_rep) 
                    salvos.append(colaborador)
                except Exception as ex:
                    erros.append("{0} - {1}".format(colaborador, ex.message))
            except Exception as e:
                erros.append("{0} - {1}".format(colaborador, e.message))
                
        return salvos, erros  
              
    def _salvar_em_rep(self, colaborador_rep):                    
        try:
            colaborador_rep.save()                
        except RelogioPontoException as e:
            if not 'cadastrado para outro' in e.message:                    
                raise e     


class ColaboradorForm(forms.ModelForm):
    salvar_em_relogios = forms.ModelMultipleChoiceField(RelogioPonto.objects.filter(ativo=True),required=False, 
                                                   label='Salvar em relógios', 
                                                   help_text='O colaborador será registrado nos relógios eletrônicos selecionados.', 
                                                   widget=forms.CheckboxSelectMultiple())
    forcar_sobrescrita = forms.BooleanField(required=False, label='Forçar sobrescrita/atualização', help_text='Sobrescreve o registro dos colaboradores que já estiverem nos relógios.')
    class Meta:
        model = Colaborador
        fields = '__all__'


    def clean_pis(self, *args, **kwargs):
        pis = (somente_numeros(self.cleaned_data['pis'])) 
        valido = validate_pis(pis)               
        if not valido:            
            raise forms.ValidationError ("PIS inválido")
        else:    
            return int(pis)
    
    
    def clean(self, *args, **kwargs): 
        cleaned_data = super(ColaboradorForm, self).clean()
        relogios_a_salvar = cleaned_data['salvar_em_relogios'].all()
        if not 'pis' in cleaned_data:
            raise forms.ValidationError ("Há problemas com o número do PIS.")  
        for relogio in relogios_a_salvar:
            pis = str(cleaned_data['pis'])
            try:
                colaboradorInREP = relogio.get_rep().colaboradores.filter(pis=pis)
            except Exception as e:
                raise forms.ValidationError('O "%s" reportou erro: %s\nVerifique se o relógio está funcionando corretamente.' % (relogio.nome, e.message ))
            if not cleaned_data['forcar_sobrescrita']: 
                if colaboradorInREP and not self.instance: 
                    raise forms.ValidationError('O "%s" reportou que um colaborador com este PIS já está cadastrado no equipamento.' % relogio.nome )
                else:
                    raise forms.ValidationError('O "%s" reportou que um colaborador precisa ser atualizado (marque a opção "Forçar sobrescrita/atualização").' % relogio.nome ) 

             
                 

    
        

    
    
                
ColaboradorFormSet = modelformset_factory(Colaborador, 
                                         form=ColaboradorForm, 
                                         extra=1, 
                                         fields=('__all__')) 




class ParametroForm(forms.ModelForm):
    model = Parametro
    
    def __init__(self, *args, **kwargs):
        super(ParametroForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if 'int' in instance.tipo:
                self.fields['valor'] = forms.IntegerField()
        
        
 
class MatriculaInlineFormSet(BaseInlineFormSet):  

    def clean(self):
        BaseInlineFormSet.clean(self) 
        for form in self.forms:
            if 'matriculas-0-DELETE' in form.data:
                raise ValidationError("Você não pode remover a primeira matrícula.")
            if not form.data['matriculas-0-numero']:
                raise ValidationError("A primeira matrícula não pode ser vazia.")



