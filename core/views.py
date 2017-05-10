# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.shortcuts import render
from core.forms import GerarArquivoForm,  ColaboradorFormSet,\
    ExportarParaRelogioForm
from django.contrib.auth import logout
from django.http.response import HttpResponse, HttpResponseForbidden,\
    HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from core.models import Colaborador, Matricula, RelogioPonto
from pyRelogioPonto.relogioponto import util
from django.utils.translation import ugettext_lazy as _
from brazilnum.pis import validate_pis
from django.views.generic.base import TemplateView
from core.util import update_afd
import json



def site_logout(request):
    logout(request)
    return HttpResponseRedirect('%s?next=%s' % (reverse('admin:login'), reverse('index')))


@login_required
def index(request): 
    return HttpResponseRedirect(reverse('admin:index'))


@login_required
def colaboradores(request): 
    title = 'Colaboradores'
    has_permission = True
    user = request.user    
    if request.POST:
        form_exportar_para_relogio = ExportarParaRelogioForm(request.POST)
    else:  
        form_exportar_para_relogio = ExportarParaRelogioForm()    
    
    return render(request, 'colaboradores.html', locals())
    

@login_required    
def gerar_arquivo(request):
    form = GerarArquivoForm(request.POST)
    if form.is_valid():   
        dados = form.gerar()
        if not dados:
            return HttpResponseRedirect(reverse('admin:index') + '?nr=1' )  
        else:   
            response = HttpResponse(dados, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="%s.txt"' % form.nome_arquivo
    else:
        response = HttpResponseForbidden(_('Requisição inválida.'))
    return response


@login_required
def recuperar_batidas(request): 
    errors = []
    if 'force' in request.GET:   
        force=True
    else:
        force=False
    
    for relogio_reg in RelogioPonto.objects.all():
        try:
            r = relogio_reg.atualizar_registros(force=force)
        except Exception as e:
            errors.append(e.message)

    result = errors != []  
       
    res = {'result': result, 'errors': errors }  
      
    return JsonResponse(res, safe=False) 


@login_required
def salvar_colaboradores(request):
    form_colaboradores = ColaboradorFormSet(request.POST)
    if form_colaboradores.is_valid():
        form_colaboradores.save()
        return HttpResponseRedirect(reverse('colaboradores') + '?salvo=1')
    return colaboradores(request)


@login_required
def importar_arquivo_csv(request):
    salvos = [] 
    erros = []  
    title = 'Colaboradores'
    has_permission = True
    user = request.user  
    try:
        file_string = handle_uploaded_file(request.FILES['arquivo_csv'])
    except:
        erros.append('Arquivo CSV inválido.')
        return render(request, 'return_importacao.html', locals()) 
    if ',' in file_string:
        separador = ','
    elif '\t' in file_string:
        separador = '\t'
    else:
        separador = ';'
    for linha in file_string.split('\n'):
        if linha:
            celulas = linha.split(separador)
            try:
                pis = celulas[1]
            except IndexError:
                pis = ''            
            if not validate_pis(pis):                
                erros.append("{0} - {1}".format(linha, _('PIS inválido')))
            else:    
                matricula_numero = celulas[2].strip()                
                if not matricula_numero or matricula_numero == '':
                    msg = "{0} - {1}".format(linha, _('Sem matrícula'))
                    erros.append(msg)
                else:
                    colaborador = Colaborador.objects.get_or_create(pis=pis)[0]
                    colaborador.nome = celulas[0]
                    colaborador.save() 
                    try:
                        matricula = Matricula.objects.get(numero=int(matricula_numero))
                    except:                    
                        matricula = Matricula()
                        matricula.numero = int(matricula_numero)                
                    matricula.colaborador = colaborador
                    matricula.save()
                    colaborador.save()
                    salvos.append(colaborador) 
            
    return render(request, 'return_importacao.html', locals())


def handle_uploaded_file(rf):
    content = ''
    for chunk in rf.chunks():
        chunk_decode = util.remover_acentos(chunk.decode('utf-8'))                   
        content ='{0}{1}'.format(content, chunk_decode)
    return content


def exportar_para_relogio(request):
    form_exportar_para_relogio = ExportarParaRelogioForm(request.POST)
    if form_exportar_para_relogio.is_valid():
        salvos, erros = form_exportar_para_relogio.exportar()        
        return render(request, 'return_importacao.html', locals())
    else:
        return colaboradores(request) 
    
    

class WelcomeAdminView(TemplateView):
    template_name = 'admin/index.html'

    
    def get(self, request, *args, **kwargs):        
        from core.sites import admin_site
        form_gerar_arquivo = GerarArquivoForm()
        messages = ['Não há registros no período selecionado.'] if 'nr' in request.GET else None
        colaborador_model = type(Colaborador)
        return admin_site.index(request, extra_context=locals())
            