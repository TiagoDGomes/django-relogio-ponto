# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.shortcuts import render
from core.forms import GerarArquivoForm,  ColaboradorFormSet,\
    ExportarParaRelogioForm
from django.contrib.auth import logout
from django.http.response import HttpResponse, HttpResponseForbidden,\
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from core.models import Colaborador, Matricula, RelogioPonto
from pyRelogioPonto.relogioponto import util
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import settings


def site_logout(request):
    logout(request)
    return HttpResponseRedirect('%s?next=/' % reverse('admin:login'))


@login_required
def index(request): 
    form_gerar_arquivo = GerarArquivoForm() 
    return render(request, 'exportar.html', locals())

@login_required
def colaboradores(request): 
    query = Colaborador.objects.all()
    paginator = Paginator(query, settings.TOTAL_PAGINACAO)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
        pagina_atual = int(page)
    except PageNotAnInteger:        
        objects = paginator.page(1)
        pagina_atual = 1
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
        pagina_atual = paginator.num_pages
    page_query = query.filter(id__in=[object.id for object in objects])
    form_colaboradores = ColaboradorFormSet(queryset=page_query)    
    paginas_range = range(1, objects.paginator.num_pages+1)
    
    form_exportar_para_relogio = ExportarParaRelogioForm()
    
    return render(request, 'colaboradores.html', locals())


@login_required    
def gerar_arquivo(request):
    form = GerarArquivoForm(request.POST)
    if form.is_valid():
        response = HttpResponse('', content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s.txt"' % form.nome_arquivo
    else:
        response = HttpResponseForbidden(_('Requisição inválida.'))
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

def exportar_para_relogio(request):
    form_exportar_para_relogio = ExportarParaRelogioForm(request.POST)
    if form_exportar_para_relogio.is_valid():
        form_exportar_para_relogio.exportar()        
        return HttpResponse('ok')
    else:
        return colaboradores(request) 
            