# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.test import TestCase
from django.urls.base import  reverse
from django.contrib import auth
from core.models import Colaborador, RelogioPonto, RegistroPonto
from datetime import datetime
import settings
from core.tests import prepare
from core import models
from django.db.models import Q
        
        
class TestPaginaInicialSemAutenticar(TestCase):
    def setUp(self):
        self.response = self.client.get('/') 

    def test_302(self):
        self.assertEqual(302, self.response.status_code) 
        
        
class TestPaginaPrincipal(prepare.PrepararParaTerUsuarioLogado):    
    def test_formulario(self):   
        self.assertContains(self.response, text='csrfmiddlewaretoken', )  
        self.assertContains(self.response, text='type="submit"',)        
        self.assertContains(self.response, text='<select ',)        
        self.assertContains(self.response, text='Formato padr',)        
        self.assertContains(self.response, text=reverse('gerar_arquivo'), )
        self.assertContains(self.response, text=reverse('site_logout'), )        
        self.assertNotContains(self.response, text='type="file"', )


        
    

        
class TestLogout(prepare.PrepararParaTerUsuarioLogado):    
    def test_logout(self):
        self.response = self.client.get(reverse('site_logout'))   
        self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response, '%s?next=/' % reverse('admin:login'))
        user = auth.get_user(self.client)   
        self.assertFalse(user.is_authenticated())   
        
        
        

            
        
class TestRelogioAddAdmin(prepare.PrepararParaCriarUsuarioAdminLogado):    
    def setUp(self):
        super(TestRelogioAddAdmin, self).setUp()
        self.response = self.client.get(reverse('admin:core_relogioponto_add'))
    
    def test_remove_save_button(self):
        self.assertNotContains(self.response, text='name="_save"')  
        
       

        
class TestPaginaColaborador(prepare.PrepararParaUsarColaboradores):       
    def test_formulario(self):          
        self.assertContains(self.response, text='csrfmiddlewaretoken',)  
        self.assertContains(self.response, text='type="submit"', count=3) # salvar, importar CSV e exportar para relógio        
        self.assertContains(self.response, text='<form', count=3)        
        self.assertNotContains(self.response, text=reverse('gerar_arquivo'), )
        self.assertContains(self.response, text=reverse('site_logout'), )
        self.assertContains(self.response, text='type="file"', )
        
        NUMERO_INPUTS_TABELACOLABORADOR = 3
        
        
        TOTAL_INPUTS_FIXOS = 4 + 5 + 2 
        self.assertContains(self.response, 'id="tabela_funcionarios"')
        numero_inputs = len(self.colaboradores) * NUMERO_INPUTS_TABELACOLABORADOR + TOTAL_INPUTS_FIXOS + NUMERO_INPUTS_TABELACOLABORADOR
        self.assertContains(self.response, text="<input ",  count=numero_inputs)          
        
        self.assertContains(self.response, text=reverse('importar_arquivo_csv'))
        self.assertContains(self.response, text=reverse('exportar_para_relogio'))
        self.assertContains(self.response, text='name="arquivo_csv"') 
        self.assertContains(self.response, text='value="Exportar"') 
        self.assertContains(self.response, text='<select') 
               
        
    def test_gravacao(self):
        self.assertEqual(len(self.colaboradores), (Colaborador.objects.count()), msg='Quantidade invalida de colaboradores registrados')
        
    def test_listar_usuarios(self):
        for colaborador in self.colaboradores:            
            self.assertContains(self.response, text=colaborador.nome)
            
    def test_matriculas(self):    
        for matricula in self.matriculas:  
            self.assertContains(self.response, text=matricula.numero)
            

class TestPaginaColaboradorExportarParaRelogio(prepare.PrepararParaUsarColaboradores, prepare.PrepararRelogio): 
    def setUp(self):
        prepare.PrepararParaUsarColaboradores.setUp(self)  
        prepare.PrepararRelogio.setUp(self)
              
    def test_relogio_listado(self):        
        self.response = self.client.get(reverse('colaboradores'))
        self.assertContains(self.response, text=self.relogio.nome) 
        
    def test_exportar_para_relogio_post(self):      
        self.response = self.client.post(reverse('exportar_para_relogio'),  {'relogio': self.relogio.id})
        self.assertTemplateUsed(self.response, template_name='return_importacao.html')
        for colaborador_sistema in models.Colaborador.objects.all(): 
            filtro = self.relogio_device.colaboradores.filter(pis=colaborador_sistema.pis)     
            if colaborador_sistema.matriculas.all().count() == 0:  
                self.assertEquals(filtro,[])
            else:
                self.assertNotEquals(filtro,[])
            
            
        
       
      
class TestObterRegistros(prepare.PrepararParaUsarColaboradores):    
    def setUp(self):
        super(TestObterRegistros, self).setUp()
        self.relogio = RelogioPonto.objects.create(nome='Teste',tipo=1)
        self.relogio.save()
        self.batida = []

        self.batida.append(RegistroPonto.objects.create(relogio=self.relogio,
                                                   data_hora=datetime.strptime('18/09/2016 10:23:45','%d/%m/%Y %H:%M:%S'),
                                                   colaborador=self.colaboradores[0],
                                                   )
                            )
        self.batida.append(RegistroPonto.objects.create(relogio=self.relogio,
                                                   data_hora=datetime.strptime('18/09/2016 17:00:12','%d/%m/%Y %H:%M:%S'),
                                                   colaborador=self.colaboradores[0],
                                                   )
                            )
        self.batida.append(RegistroPonto.objects.create(relogio=self.relogio,
                                                   data_hora=datetime.strptime('19/10/2016 10:25:00','%d/%m/%Y %H:%M:%S'),
                                                   colaborador=self.colaboradores[0]
                                                   )
                            )
        self.batida.append(RegistroPonto.objects.create(relogio=self.relogio,
                                                   data_hora=datetime.strptime('19/10/2016 16:59:12','%d/%m/%Y %H:%M:%S'),
                                                   colaborador=self.colaboradores[0]
                                                   )
                            )
        self.batida.append(RegistroPonto.objects.create(relogio=self.relogio,
                                                   data_hora=datetime.strptime('17/10/2016 07:25:00','%d/%m/%Y %H:%M:%S'),
                                                   colaborador=self.colaboradores[1]
                                                   )
                            )
        self.batida.append( RegistroPonto.objects.create(relogio=self.relogio,
                                                   data_hora=datetime.strptime('18/10/2016 12:00:00','%d/%m/%Y %H:%M:%S'),
                                                   colaborador=self.colaboradores[1]
                                                   )
                           )               
        
        
        self.batida.append( RegistroPonto.objects.create(relogio=self.relogio,
                                                   data_hora=datetime.strptime('18/10/2016 12:05:00','%d/%m/%Y %H:%M:%S'),
                                                   colaborador=self.colaboradores[2]
                                                   )
                           )
        
        
        
        
        
        self.formato = [('matricula',15), 
                   ('datahora', "%d%m%y%H%M"),
                   ('personalizado','00100100'),
                  ]
        self.batida_texto1 = self.batida[0].converter_em_texto(self.formato) 
        self.batida_texto2 = self.batida[1].converter_em_texto(self.formato) 
        self.batida_texto3 = self.batida[5].converter_em_texto(self.formato)                
        self.batida_texto4 = self.batida[6].converter_em_texto(self.formato)                
        #self.formato_exportacao = FormatoExportacao(nome='TestN', formato=self.formato)    
    
    
    def test_converter(self):        
        self.assertTrue('000000000123456180916102300100100' in self.batida_texto1)      
        self.assertTrue('000000000123456180916170000100100' in self.batida_texto2)
        self.assertFalse('123456' in self.batida_texto3)
        self.assertFalse('789012' in self.batida_texto3)        
        self.assertEquals('' , self.batida_texto3) # não tem matricula        
        self.assertTrue('000000000747479181016120500100100' in self.batida_texto4)
        
        
    def test_converter_outro_formato(self):        
        formato_com_pis = [
                   ('datahora', "%d%m%y%H%M"),
                   ('personalizado','xxx'),
                   ('pis',15), 
                  ]
        texto = self.batida[5].converter_em_texto(formato_com_pis)                
        self.assertTrue('1810161200xxx000034644028941' in texto)
        
    
         
    def test_obter(self):        
        self.response = self.client.post(reverse('gerar_arquivo'), {'inicio': '18/10/2016',
                                                                    'fim': '19/10/2016', 
                                                                    'formato': 'default',
                                                                    })
        self.assertEqual(200, self.response.status_code)   
        self.assertTrue('Content-Disposition' in self.response) 
        self.assertTrue('2016-10-18.2016-10-19.txt' in self.response['Content-Disposition'], msg='Nome errado de arquivo' )
        self.assertNotContains(self.response, self.batida_texto1)
        self.assertNotContains(self.response, self.batida_texto2)
        self.assertContains(self.response, self.batida_texto3)
        
        # segunda tentativa, mesma data no inicio e fim
        self.response = self.client.post(reverse('gerar_arquivo'), {'inicio': '19/10/2016',
                                                                    'fim': '19/10/2016', 
                                                                    'formato': 'default',
                                                                    })
        self.assertEqual(200, self.response.status_code)   
        self.assertTrue('Content-Disposition' in self.response) 
        self.assertTrue('"2016-10-19.txt' in self.response['Content-Disposition'], msg='Nome errado de arquivo' )
        self.assertNotContains(self.response, self.batida_texto1)
        self.assertNotContains(self.response, self.batida_texto2)
        self.assertContains(self.response, self.batida_texto3)
        

    def test_obter_nada(self):        
        self.response = self.client.post(reverse('gerar_arquivo'), {'inicio': '01/01/1999',
                                                                    'fim': '01/01/2000', 
                                                                    'formato': 'default',
                                                                    })
        redir_url = reverse('index') + '?nr=1'
        self.assertEqual(302, self.response.status_code)  
        self.assertRedirects(self.response, redir_url)
         
        self.assertFalse('Content-Disposition' in self.response) 
        self.response = self.client.get(redir_url)
        self.assertContains(self.response , 'Não há registros no período selecionado.') 
        

        
        
class TestColaboradorInvalido(prepare.PrepararParaCriarUsuarioAdminLogado):
    def test_pis_invalido(self):        
        self.response_post = self.client.post(reverse('salvar_colaboradores'), {
                                                           'form-TOTAL_FORMS': 1,
                                                           'form-INITIAL_FORMS': 0,
                                                           'form-MIN_NUM_FORMS': 0,
                                                           'form-MAX_NUM_FORMS': 1000,
                                                          # 'form-0-id': '', 
                                                           'form-0-nome': 'Teste', 
                                                           'form-0-pis': '0101', 
                                                           'form-0-matriculas': '666222\n777333',
                                                        }) 
        self.assertNotContains(self.response_post, 'Colaborador com este PIS j')
        self.assertContains(self.response_post, 'PIS inválido')
        
    def test_matricula_invalida(self):        
        self.response_post = self.client.post(reverse('salvar_colaboradores'), {
                                                           'form-TOTAL_FORMS': 1,
                                                           'form-INITIAL_FORMS': 0,
                                                           'form-MIN_NUM_FORMS': 0,
                                                           'form-MAX_NUM_FORMS': 1000,
                                                          # 'form-0-id': '', 
                                                           'form-0-nome': 'Teste', 
                                                           'form-0-pis': '30341726658', 
                                                           'form-0-matriculas': '343X434',
                                                        })    
        
        self.assertRedirects(self.response_post, reverse('colaboradores') + '?salvo=1')
        
        
class TestColaboradoresPost(prepare.PrepararParaUsarColaboradores):         
    
    def test_alteracoes(self):
        self.pis_antigo = self.colaboradores[0].pis        
        self.novo_nome = 'TesteSalvar'
        pis = '50750683739'
        self.response_post = self.client.post(reverse('salvar_colaboradores'), {
                                                           'form-TOTAL_FORMS': 2,
                                                           'form-INITIAL_FORMS': 1,
                                                           'form-MIN_NUM_FORMS': 0,
                                                           'form-MAX_NUM_FORMS': 1000,
                                                           'form-0-id': self.colaboradores[0].id, 
                                                           'form-0-nome': self.novo_nome, 
                                                           'form-0-pis': pis, 
                                                           'form-0-matriculas': '666222\n777333',
                                                        }) 
        url =  reverse('colaboradores') + '?salvo=1'  
        self.assertRedirects(self.response_post, expected_url=url)   
           
        self.response_get2 = self.client.get(url)
        self.assertContains(self.response_get2, 'id="info-save"')  
        
        self.assertNotContains(self.response_get2, self.pis_antigo)
        self.assertContains(self.response_get2, pis)
        
        
    
        
        colaborador_salvo = Colaborador.objects.get(pis=pis)
        self.assertEqual(colaborador_salvo.nome, 'TesteSalvar', 'Nome nao foi salvo')
        self.assertEquals(colaborador_salvo.matriculas.filter(numero=666222).count(), 1)
        self.assertEquals(colaborador_salvo.matriculas.filter(numero=777333).count(), 1)

        self.assertNotContains(self.response_get2, text=self.matricula_antiga1)
        self.assertNotContains(self.response_get2, text=self.matricula_antiga2)
        self.assertContains(self.response_get2, text='666222', count=1)
        self.assertContains(self.response_get2, text='777333', count=1)
        
                      
                    
class TestImportarArquivoCSV(prepare.PrepararParaImportacao):    
    def test_resposta(self):        
        self.assertEquals(Colaborador.objects.filter(nome__contains=' VALIDO').count(), self.total_validos)
        self.assertEquals(Colaborador.objects.filter(nome__contains='INVALIDO').count(), 0)
        self.assertContains(self.response,'INVALIDO', count=self.total_invalidos)
        self.assertContains(self.response,'erro', count=self.total_invalidos)
        self.assertContains(self.response,'registrado', count=self.total_validos)
        self.assertTemplateUsed(self.response, template_name='return_importacao.html')
        

class TestPaginacaoColaboradores(prepare.PrepararParaImportacao):
    def setUp(self):
        prepare.PrepararParaImportacao.setUp(self)
        self.colaboradores = Colaborador.objects.all()        

    def test_primeira_pagina(self):
        count = 0
        self.response = self.client.get(reverse('colaboradores'))
        self.assertContains(self.response, 'class="pagination')
        
        for colaborador in self.colaboradores:
            count+=1
            if count <= settings.TOTAL_PAGINACAO:
                self.assertContains(self.response, colaborador.nome)
            else:
                self.assertNotContains(self.response, colaborador.nome)        

    def test_segunda_pagina(self):
        count = 0
        self.response = self.client.get(reverse('colaboradores') + '?page=2')
        for colaborador in self.colaboradores:
            count+=1            
            if count <= settings.TOTAL_PAGINACAO:
                self.assertNotContains(self.response, colaborador.nome)
            else:
                self.assertContains(self.response, colaborador.nome)
                

    
                

 

                

