# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django import forms
from django.forms import widgets
from core.models import Colaborador, Matricula
from django.forms.widgets import Textarea
from django.forms.models import modelformset_factory


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput())
    

class GerarArquivoForm(forms.Form):
    inicio = forms.DateField()
    fim = forms.DateField()
    formato = forms.ChoiceField(choices=[('default','Formato padrão')], label='Formato')
    @property
    def nome_arquivo(self):
        return "{0}-{1}".format( self.cleaned_data['inicio'].strftime('%d%m%Y'), self.cleaned_data['fim'].strftime('%d%m%Y'))
    

class ColaboradorForm(forms.ModelForm):
    matriculas = forms.CharField(widget=Textarea(attrs={'rows':1, 'cols':6,}), required=False)
    
    class Meta:
        model = Colaborador
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ColaboradorForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            colaborador = kwargs['instance']
            self.initial['matriculas'] = "\n".join ( str(m.numero) for m in colaborador.matriculas.all() ) 
 
    def save(self, *args, **kwargs):
        super(ColaboradorForm, self).save(*args, **kwargs)
        matriculas_post = self.cleaned_data['matriculas'].split('\n')        

        self.instance.matriculas.all().delete()
        self.instance.save()
        for numero_a_salvar in matriculas_post:
            if numero_a_salvar:
                matricula = Matricula()
                matricula.numero = numero_a_salvar
                matricula.colaborador = self.instance
                #matricula.colaborador.save()
               
                matricula.save()
 
ColaboradorFormSet = modelformset_factory(Colaborador, 
                                         form=ColaboradorForm, 
                                         extra=1, 
                                         fields=('__all__')) 
