# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.shortcuts import render
from core.forms import GerarArquivoForm, ColaboradorForm, ColaboradorFormSet
from django.contrib.auth import logout
from django.http.response import HttpResponse, HttpResponseForbidden,\
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from core.models import Colaborador, Matricula
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from pprint import pprint
from pyRelogioPonto.relogioponto import util


def site_logout(request):
    logout(request)
    return HttpResponseRedirect('%s?next=/' % reverse('admin:login'))


@login_required
def index(request): 
    form_gerar_arquivo = GerarArquivoForm() 
    return render(request, 'exportar.html', locals())

@login_required
def colaboradores(request): 
    form_colaboradores = ColaboradorFormSet()
    return render(request, 'colaboradores.html', locals())


@login_required    
def gerar_arquivo(request):
    form = GerarArquivoForm(request.POST)
    if form.is_valid():
        response = HttpResponse('', content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s.txt"' % form.nome_arquivo
    else:
        response = HttpResponseForbidden('Requisição inválida.')
    return response


@login_required
def salvar_colaboradores(request):
    form_colaboradores = ColaboradorFormSet(request.POST)
    if form_colaboradores.is_valid():
        form_colaboradores.save()
    return HttpResponseRedirect(reverse('colaboradores'))

@login_required
def importar_arquivo_csv(request):    
    for linha in handle_uploaded_file(request.FILES['arquivo_csv']).split('\n'):
        if linha:
            celulas = linha.split(',')
            colaborador = Colaborador.objects.get_or_create(pis=int(celulas[1]))[0]
            colaborador.nome = celulas[0]
            colaborador.save()
            if celulas[2].strip():
                try:
                    matricula = Matricula.objects.get(numero=int(celulas[2]))
                except:                    
                    matricula = Matricula()
                    matricula.numero = int(celulas[2])
                
                matricula.colaborador = colaborador
                matricula.save()
            colaborador.save()
    return HttpResponseRedirect(reverse('index'))


def handle_uploaded_file(rf):
    content = ''
    for chunk in rf.chunks():
        chunk_decode = util.remover_acentos(chunk.decode('utf-8'))                   
        content ='{0}{1}'.format(content, chunk_decode)
    return content
            