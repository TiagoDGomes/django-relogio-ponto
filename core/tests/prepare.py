# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.test import TestCase
from core.models import Colaborador, Matricula
from django.contrib.auth.models import User
from django.urls.base import reverse
from settings import BASE_DIR
import os

class PrepararParaCriarUsuarioLogado(TestCase):   
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234qwer')
        self.logged_in = self.client.login(username='testuser', password='1234qwer')



class PrepararParaCriarUsuarioAdminLogado(PrepararParaCriarUsuarioLogado):
    def setUp(self):
        PrepararParaCriarUsuarioLogado.setUp(self)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
    


class PrepararParaTerUsuarioLogado(PrepararParaCriarUsuarioLogado):   
    def setUp(self):        
        super(PrepararParaTerUsuarioLogado, self).setUp()
        self.response = self.client.get('/')

        
             
class PrepararParaUsarColaboradores(PrepararParaTerUsuarioLogado): 
    def setUp(self):    
        
        self.colaboradores = []
        
        
        # Colaborador com 2 matrículas
        colaborador = Colaborador()
        colaborador.nome = 'Teste 1'
        colaborador.pis = '700.85016.25-0'
        colaborador.save()
        self.matricula_antiga1 = '123456'
        self.matricula_antiga2 = '789012'
        
        self.colaboradores.append(colaborador)    
        matricula = Matricula()
        matricula.numero = self.matricula_antiga1
        matricula.colaborador = colaborador
        matricula.save()
        
        matricula2 = Matricula()
        matricula2.numero = self.matricula_antiga2
        matricula2.colaborador = colaborador
        matricula2.save()
        
        self.matriculas = []
        self.matriculas.append(matricula)
        self.matriculas.append(matricula2)
        
        # Colaborador sem matrícula   
        colaborador = Colaborador()
        colaborador.nome = 'Teste 2'
        colaborador.pis = '346.44028.94-1'
        colaborador.save()
        
        self.colaboradores.append(colaborador)
        
        
        # Colaborador com uma matrícula
        colaborador = Colaborador()
        colaborador.nome = 'Teste 3'
        colaborador.pis = '515.86503.41-7'
        colaborador.save()
        
        matricula = Matricula()
        matricula.numero = '747479'
        matricula.colaborador = colaborador
        matricula.save()
        
        
        
        self.colaboradores.append(colaborador)
        
        
        
        
        super(PrepararParaUsarColaboradores, self).setUp()    
        self.response = self.client.get(reverse('colaboradores'))

 
class PrepararParaImportacao(PrepararParaTerUsuarioLogado):  
    def setUp(self):
        PrepararParaTerUsuarioLogado.setUp(self)  
        self.total = 0
        with open(os.path.join(BASE_DIR, 'exemplo_colaboradores.csv')) as f:                      
            self.total = len(str(f.read()).encode('utf-8').split('\n'))
        with open(os.path.join(BASE_DIR, 'exemplo_colaboradores.csv')) as csv_file:  
            self.client.post(reverse('importar_arquivo_csv'), {'arquivo_csv': csv_file})     


