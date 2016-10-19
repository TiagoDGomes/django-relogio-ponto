from django.shortcuts import render
from core.forms import LoginForm
from django.contrib.auth import authenticate

def index(request):
    if not request.POST:
        form = LoginForm() 
    else:
        username = request.POST['username']
        password = request.POST['password']
        request.user = authenticate(username=username, password=password)
        
    template = 'index.html' if not request.user.is_anonymous() else 'login.html'
    
    return render(request, template, locals())

    
