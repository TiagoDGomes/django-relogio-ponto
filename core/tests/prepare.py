# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.test import TestCase
from core.models import Colaborador, Matricula
from django.contrib.auth.models import User
from django.urls.base import reverse
from settings import BASE_DIR
import os
import settings
from pyRelogioPonto import relogioponto
from core import models



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
            lines = (str(f.read()).encode('utf-8')).split('\n')
            self.total = len(lines)
            self.total_validos = 0
            self.total_invalidos = 0
            
            for line in lines:
                if 'INVALIDO' in line:
                    self.total_invalidos += 1
                else:
                    self.total_validos += 1
             
        with open(os.path.join(BASE_DIR, 'exemplo_colaboradores.csv')) as csv_file:  
            self.response = self.client.post(reverse('importar_arquivo_csv'), {'arquivo_csv': csv_file})     


class PrepararRelogio(TestCase):
    def setUp(self):        
        if not settings.TEST_RELOGIO_PONTO_ENDERECO:
            raise Exception('Não há endereço definido para TEST_RELOGIO_PONTO_ENDERECO em settings')
        if settings.TEST_RELOGIO_PONTO_TIPO == 0:
            raise Exception('Não é possível fazer testes com o relógio de ponto definido em settings.')
        
        self.relogio = models.RelogioPonto()
        self.relogio.nome = 'Teste de relogio'        
        self.relogio.tipo, self.relogio_nome, self.RelogioPontoTipo, _ = relogioponto.base.get_rep_suportados()[0]
        self.relogio.save() 
        
        parametro = self.relogio.parametros.get(propriedade='endereco') 
        parametro.valor = settings.TEST_RELOGIO_PONTO_ENDERECO
        parametro.save()
        
        parametro = self.relogio.parametros.get(propriedade='porta') 
        if settings.TEST_RELOGIO_PONTO_PORTA:            
            parametro.valor = settings.TEST_RELOGIO_PONTO_PORTA
            parametro.save()
        else:
            parametro.delete()
            
            
        self.relogio_device = self.relogio.get_rep()
        self.relogio_device.conectar()
        
    def tearDown(self):        
        self.relogio_device.desconectar()    
