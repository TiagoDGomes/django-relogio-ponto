from django.test import TestCase
from django.contrib.auth.models import User
from django.urls.base import  reverse
from django.contrib import auth
from core.models import Colaborador, Matricula



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
        self.assertContains(self.response, text='csrfmiddlewaretoken')  
        self.assertContains(self.response, text='<input', count=8)
        self.assertContains(self.response, text='type="submit"', count=2)        
        self.assertContains(self.response, text=reverse('gerar_arquivo'), )
        self.assertContains(self.response, text=reverse('site_logout'), )
        self.assertContains(self.response, text='type="file"', )
    
    def test_nenhum_colaborador_registrado(self):
        self.assertContains(self.response, text='Nenhum colaborador registrado')
        
    

        
class TestLogout(TestUseParaUsuarioLogado):
    
    def test_logout(self):
        self.response = self.client.get(reverse('site_logout'))   
        self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response, '%s?next=/' % reverse('admin:login'))
        user = auth.get_user(self.client)   
        self.assertFalse(user.is_authenticated())   
        
class TestGerarArquivo(TestUseParaUsuarioLogado):
    
    def setUp(self):
        super(TestGerarArquivo, self).setUp()
        self.response = self.client.post(reverse('gerar_arquivo'), {'inicio': '18/10/2016', 'fim': '19/10/2016'}) 
         
    def test_ok(self):
        self.assertEqual(200, self.response.status_code)   
        self.assertTrue('Content-Disposition' in self.response) 
        self.assertTrue('18102016-19102016.txt' in self.response['Content-Disposition'], msg='Nome errado de arquivo' )
        
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
        
        self.colaboradores.append(colaborador)    
        matricula = Matricula()
        matricula.colaborador = colaborador
        matricula.numero = '111111112'
        matricula.save()
        
        matricula2 = Matricula()
        matricula2.colaborador = colaborador
        matricula2.numero = '757575'
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
        
        
class TestCaseColaboradores(TestUseColaboradores):
    def test_gravacao(self):
        self.assertEqual(len(self.colaboradores), (Colaborador.objects.count()), msg='Quantidade invalida de colaboradores registrados')
        
    def test_listar_usuarios(self):
        for colaborador in self.colaboradores:            
            self.assertContains(self.response, text=colaborador.nome)
            
    def test_matriculas(self):    
        for matricula in self.matriculas:       
            print(matricula)         
            self.assertContains(self.response, text=matricula.numero)
           
    def test_tabela_funcionarios(self):
        self.assertContains(self.response, 'id="tabela_funcionarios"')    

