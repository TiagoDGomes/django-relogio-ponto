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
        print (self.cleaned_data)
        return "{0}-{1}".format( self.cleaned_data['inicio'].strftime('%d%m%Y'), self.cleaned_data['fim'].strftime('%d%m%Y'))
        