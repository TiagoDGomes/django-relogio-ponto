from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput())

class GerarArquivoForm(forms.Form):
    inicio = forms.DateField()
    fim = forms.DateField()
    
    @property
    def nome_arquivo(self):
        return "{1}-{2}".format( self.cleaned_data('inicio').strptime('%d%m%Y'), self.cleaned_data('fim').strptime('%d%m%Y'))
        