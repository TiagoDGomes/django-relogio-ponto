from django.shortcuts import render
from core.forms import LoginForm, GerarArquivoForm
from django.contrib.auth import authenticate
from django.http.response import HttpResponse, HttpResponseForbidden

def index(request):
    if not request.POST:
        form = LoginForm() 
    else:
        username = request.POST['username']
        password = request.POST['password']
        request.user = authenticate(username=username, password=password)
    
    form_gerar_arquivo = GerarArquivoForm()    
    template = 'index.html' if not request.user.is_anonymous() else 'login.html'
    
    return render(request, template, locals())

    
def gerar_arquivo(request):
    form = GerarArquivoForm(request.POST)
    if form.is_valid():
        response = HttpResponse('', content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s.txt"' % form.nome_arquivo
    else:
        response = HttpResponseForbidden()
    return response