# -*- coding: utf-8 -*-
from __future__ import unicode_literals 

'''
Criado em 9 de dez de 2016

@author: tiago.gomes
'''

from django.test import TestCase
from django.urls.base import reverse
from core.tests import prepare
from core.models import Colaborador


class TestPaginaInicialAdmin(prepare.PrepararParaCriarUsuarioAdminLogado):
    def setUp(self):
        prepare.PrepararParaCriarUsuarioAdminLogado.setUp(self)
        self.response = self.client.get(reverse('admin:index'))
        
    def test_conteudo(self):        
        self.assertContains(self.response, 'Colaboradores')
        self.assertContains(self.response, 'Relógios de ponto')
        self.assertNotContains(self.response, 'Administração do Django')
        self.assertNotContains(self.response, 'Administração do site')
        self.assertNotContains(self.response, 'Ver o site')
        self.assertTemplateUsed(self.response, template_name='part/exportar_part.html')
    
    def test_formulario(self):          
        self.assertContains(self.response, text='csrfmiddlewaretoken', )  
        self.assertContains(self.response, text='type="submit"',)        
        self.assertContains(self.response, text='<select ',)        
        self.assertContains(self.response, text='Formato padr',)        
        self.assertContains(self.response, text=reverse('gerar_arquivo'), )
        self.assertContains(self.response, text=reverse('admin:logout'), )        
        self.assertNotContains(self.response, text='type="file"', )
        
        
            
        
class TestRelogioAddAdmin(prepare.PrepararParaCriarUsuarioAdminLogado):    
    def setUp(self):
        super(TestRelogioAddAdmin, self).setUp()
        self.response = self.client.get(reverse('admin:core_relogioponto_add'))
    
    def test_remove_save_button(self):
        self.assertNotContains(self.response, text='name="_save"')          
    

class TestPaginacaoColaboradores(prepare.PrepararParaImportacao):      
        
    def test_paginas(self):
        self.colaboradores = Colaborador.objects.all()        
        self.response = self.client.get(reverse('admin:core_colaborador_changelist'))
        for colaborador in self.colaboradores:
            self.assertContains(self.response, colaborador.nome)
