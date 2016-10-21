from django.test import TestCase
from django.contrib.auth.models import User
from django.urls.base import  reverse
from django.contrib import auth



class TestCaseParaCriarUsuarioLogado(TestCase):   
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234qwer')
        self.logged_in = self.client.login(username='testuser', password='1234qwer')

class TestCaseParaCriarUsuarioAdminLogado(TestCaseParaCriarUsuarioLogado):
    def setUp(self):
        TestCaseParaCriarUsuarioLogado.setUp(self)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
    

class TestCaseParaUsuarioLogado(TestCaseParaCriarUsuarioLogado):   
    def setUp(self):        
        super(TestCaseParaUsuarioLogado, self).setUp()
        self.response = self.client.get('/')
        
        
class TestPaginaInicialSemAutenticar(TestCase):

    def setUp(self):
        self.response = self.client.get('/') 

    def test_302(self):
        self.assertEqual(302, self.response.status_code)        
        
        
class TestPaginaPrincipal(TestCaseParaUsuarioLogado):
    
    def test_formulario(self):   
        self.assertContains(self.response, text='csrfmiddlewaretoken')  
        self.assertContains(self.response, text='<input', count=5)
        self.assertContains(self.response, text='type="submit"', )        
        self.assertContains(self.response, text=reverse('gerar_arquivo'), )
        self.assertContains(self.response, text=reverse('site_logout'), )
    
    def test_tabela_funcionarios(self):
        self.assertContains(self.response, 'id="tabela_funcionarios"')
        
class TestLogout(TestCaseParaUsuarioLogado):
    
    def test_logout(self):
        self.response = self.client.get(reverse('site_logout'))   
        self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response, '%s?next=/' % reverse('admin:login'))
        user = auth.get_user(self.client)   
        self.assertFalse(user.is_authenticated())   
        
class TestGerarArquivo(TestCaseParaUsuarioLogado):
    
    def setUp(self):
        super(TestGerarArquivo, self).setUp()
        self.response = self.client.post(reverse('gerar_arquivo'), {'inicio': '18/10/2016', 'fim': '19/10/2016'}) 
         
    def test_ok(self):
        self.assertEqual(200, self.response.status_code)   
        self.assertTrue('Content-Disposition' in self.response) 
        self.assertTrue('18102016-19102016.txt' in self.response['Content-Disposition'], msg='Nome errado de arquivo' )
        
class TestRelogioAddAdmin(TestCaseParaCriarUsuarioAdminLogado):
    
    def setUp(self):
        super(TestRelogioAddAdmin, self).setUp()
        self.response = self.client.get(reverse('admin:core_relogioponto_add'))
    
    def test_remove_save_button(self):
        self.assertNotContains(self.response, text='name="_save"')  
        
             
        
        

