from django.test import TestCase
from django.contrib.auth.models import User
from django.urls.base import  reverse
from django.contrib import auth
from core.models import Colaborador, Matricula, RelogioPonto, RegistroPonto
from settings import BASE_DIR
import os
from datetime import datetime

''''
TOTAL_SUBMITS = 3
TOTAL_INPUT_TEXT_FIXOS = 2
TOTAL_INPUT_FILE_FIXOS = 1
TOTAL_INPUT_CHECKBOX = 1
TOTAL_CSRFTOKEN = 3
NUMERO_INPUTS_TABELACOLABORADOR = 3
TOTAL_MANAGEMENTFORM = 1
TOTAL_INPUTS_FIXOS = TOTAL_MANAGEMENTFORM*4 + TOTAL_SUBMITS + TOTAL_INPUT_TEXT_FIXOS +  TOTAL_INPUT_FILE_FIXOS +  TOTAL_INPUT_CHECKBOX +  TOTAL_CSRFTOKEN
'''

class TestUseParaCriarUsuarioLogado(TestCase):   
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234qwer')
        self.logged_in = self.client.login(username='testuser', password='1234qwer')



class TestUseParaCriarUsuarioAdminLogado(TestUseParaCriarUsuarioLogado):
    def setUp(self):
        TestUseParaCriarUsuarioLogado.setUp(self)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
    


class TestUseParaUsuarioLogado(TestUseParaCriarUsuarioLogado):   
    def setUp(self):        
        super(TestUseParaUsuarioLogado, self).setUp()
        self.response = self.client.get('/')
        
        
        
class TestPaginaInicialSemAutenticar(TestCase):

    def setUp(self):
        self.response = self.client.get('/') 

    def test_302(self):
        self.assertEqual(302, self.response.status_code)        
        
        
        
class TestPaginaPrincipal(TestUseParaUsuarioLogado):
    
    def test_formulario(self):   
        self.assertContains(self.response, text='csrfmiddlewaretoken', )  
        self.assertContains(self.response, text='type="submit"',)        
        self.assertContains(self.response, text=reverse('gerar_arquivo'), )
        self.assertContains(self.response, text=reverse('site_logout'), )        
        self.assertNotContains(self.response, text='type="file"', )


        
    

        
class TestLogout(TestUseParaUsuarioLogado):
    
    def test_logout(self):
        self.response = self.client.get(reverse('site_logout'))   
        self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response, '%s?next=/' % reverse('admin:login'))
        user = auth.get_user(self.client)   
        self.assertFalse(user.is_authenticated())   
        
        
        

            
        
class TestRelogioAddAdmin(TestUseParaCriarUsuarioAdminLogado):
    
    def setUp(self):
        super(TestRelogioAddAdmin, self).setUp()
        self.response = self.client.get(reverse('admin:core_relogioponto_add'))
    
    def test_remove_save_button(self):
        self.assertNotContains(self.response, text='name="_save"')  
        
        
             
class TestUseColaboradores(TestUseParaUsuarioLogado): 
    def setUp(self):    
        
        self.colaboradores = []
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
        
           
        colaborador = Colaborador()
        colaborador.nome = 'Teste 2'
        colaborador.pis = '346.44028.94-1'
        colaborador.save()
        
        self.colaboradores.append(colaborador)
        super(TestUseColaboradores, self).setUp()    
        self.response = self.client.get(reverse('colaboradores'))

        
        

        
class TestPaginaColaborador(TestUseColaboradores):
    
    
    def test_formulario(self):  
        
        self.assertContains(self.response, text='csrfmiddlewaretoken',)  
        self.assertContains(self.response, text='type="submit"', count=2)        
        self.assertNotContains(self.response, text=reverse('gerar_arquivo'), )
        self.assertContains(self.response, text=reverse('site_logout'), )
        self.assertContains(self.response, text='type="file"', )
        
        NUMERO_INPUTS_TABELACOLABORADOR = 3
        
        TOTAL_INPUTS_FIXOS = 9
        self.assertContains(self.response, 'id="tabela_funcionarios"')
        numero_inputs = len(self.colaboradores) * NUMERO_INPUTS_TABELACOLABORADOR + TOTAL_INPUTS_FIXOS + NUMERO_INPUTS_TABELACOLABORADOR
        self.assertContains(self.response, text="<input ",  count=numero_inputs)          
        
        self.assertContains(self.response, text=reverse('importar_arquivo_csv'))
        self.assertContains(self.response, text='name="arquivo_csv"')        
        
    def test_gravacao(self):
        self.assertEqual(len(self.colaboradores), (Colaborador.objects.count()), msg='Quantidade invalida de colaboradores registrados')
        
    def test_listar_usuarios(self):
        for colaborador in self.colaboradores:            
            self.assertContains(self.response, text=colaborador.nome)
            
    def test_matriculas(self):    
        for matricula in self.matriculas:  
            self.assertContains(self.response, text=matricula.numero)
           
  
        
  
      
class TestObterRegistros(TestUseColaboradores):
    
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
        
        
        
        
        self.response = self.client.post(reverse('gerar_arquivo'), {'inicio': '18/10/2016', 'fim': '19/10/2016'})
     
    
    
    def test_converter(self):
        formato = [('matricula',15), 
                   ('datahora', "%d%m%y%H%M"),
                   ('personalizado','00100100'),
                  ]
        texto = self.batida[0].converter_em_texto(formato)        
        self.assertTrue('000000000123456180916102300100100' in texto)
        texto = self.batida[1].converter_em_texto(formato)                
        self.assertTrue('000000000123456180916170000100100' in texto)      
        texto = self.batida[5].converter_em_texto(formato)                
        self.assertFalse('123456' in texto)
        self.assertFalse('789012' in texto)
        self.assertEquals('' , texto)
        formato = [('pis',15), 
                   ('datahora', "%d%m%y%H%M"),
                   ('personalizado','00100100'),
                  ]
        
        texto = self.batida[5].converter_em_texto(formato)                
        self.assertTrue('000034644028941181016120000100100' in texto)
        
        
         
    def test_obter(self):
        self.assertEqual(200, self.response.status_code)   
        self.assertTrue('Content-Disposition' in self.response) 
        self.assertTrue('18102016-19102016.txt' in self.response['Content-Disposition'], msg='Nome errado de arquivo' )        
        #self.assertContains(self.batida[0], PadraoExportacao.gerar_com(self.response))
        
    #def test_resultado(self):
        

        

class TestCaseColaboradoresPost(TestUseColaboradores):
    def test_alteracoes(self):
        self.pis_antigo = self.colaboradores[0].pis        
        self.novo_nome = 'TesteSalvar'
        self.response_post = self.client.post(reverse('salvar_colaboradores'), {
                                                           'form-TOTAL_FORMS': 2,
                                                           'form-INITIAL_FORMS': 1,
                                                           'form-MIN_NUM_FORMS': 0,
                                                           'form-MAX_NUM_FORMS': 1000,
                                                           'form-0-id': self.colaboradores[0].id, 
                                                           'form-0-nome': self.novo_nome, 
                                                           'form-0-pis': '4441234444', 
                                                           'form-0-matriculas': '666222\n777333',
                                                        }) 
           
        self.assertRedirects(self.response_post, expected_url=reverse('colaboradores'))
        self.response_get2 = self.client.get(reverse('colaboradores'))
        self.assertNotContains(self.response_get2, self.pis_antigo)
        self.assertContains(self.response_get2, '4441234444')
        
    
        
        colaborador_salvo = Colaborador.objects.get(pis='4441234444')
        self.assertEqual(colaborador_salvo.nome, 'TesteSalvar', 'Nome nao foi salvo')
        self.assertEquals(colaborador_salvo.matriculas.filter(numero=666222).count(), 1)
        self.assertEquals(colaborador_salvo.matriculas.filter(numero=777333).count(), 1)

        self.assertNotContains(self.response_get2, text=self.matricula_antiga1)
        self.assertNotContains(self.response_get2, text=self.matricula_antiga2)
        self.assertContains(self.response_get2, text='666222', count=1)
        self.assertContains(self.response_get2, text='777333', count=1)
        

        
class TestCaseImportarArquivoCSV(TestUseParaUsuarioLogado):

    
    def test_submit(self):
        with open(os.path.join(BASE_DIR, 'exemplo_colaboradores.csv')) as csv_file:
            self.client.post(reverse('importar_arquivo_csv'), {'arquivo_csv': csv_file})              
        self.assertEquals(Colaborador.objects.filter(nome__contains='CSV_').count(), 3)

 
            

