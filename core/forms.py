from django import forms
from django.forms import widgets
from core.models import Colaborador
from django.forms.widgets import Textarea

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput())

class GerarArquivoForm(forms.Form):
    inicio = forms.DateField()
    fim = forms.DateField()
    
    @property
    def nome_arquivo(self):
        return "{0}-{1}".format( self.cleaned_data['inicio'].strftime('%d%m%Y'), self.cleaned_data['fim'].strftime('%d%m%Y'))

class ColaboradorForm(forms.ModelForm):
    matriculas = forms.CharField(widget=Textarea(attrs={'rows':2, 'cols':6}))
    
    class Meta:
        model = Colaborador
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ColaboradorForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            colaborador = kwargs['instance']
            self.initial['matriculas'] = "\n".join ( str(m.numero) for m in colaborador.matriculas.all() ) 
    