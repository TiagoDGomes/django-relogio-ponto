from django.shortcuts import render
from core.forms import GerarArquivoForm
from django.contrib.auth import logout
from django.http.response import HttpResponse, HttpResponseForbidden,\
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from core.models import Colaborador, Matricula
from django.forms.formsets import formset_factory


def site_logout(request):
    logout(request)
    return HttpResponseRedirect('%s?next=/' % reverse('admin:login'))


@login_required
def index(request): 
    form_gerar_arquivo = GerarArquivoForm() 
    colaboradores = Colaborador.objects.all()
    colaboradores_mf = formset_factory(Colaborador,extra=0)()
    print(colaboradores_mf)
    return render(request, 'index.html', locals())


@login_required    
def gerar_arquivo(request):
    form = GerarArquivoForm(request.POST)
    if form.is_valid():
        response = HttpResponse('', content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s.txt"' % form.nome_arquivo
    else:
        response = HttpResponseForbidden()
    return response

