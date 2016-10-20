from django.test import TestCase
from django.contrib.auth.models import User
from django.urls.base import resolve, reverse
from pprint import pprint

class TestCaseParaUsuarioLogado(TestCase):   
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234qwer')
        self.logged_in = self.client.login(username=self.user.username, password='1234qwer')
        self.response = self.client.get('/', follow=True)
        
         
class TestPaginaInicialSemAutenticar(TestCase):

    def setUp(self):
        self.response = self.client.get('/') 

    def test_200(self):
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'login.html')
    
    def test_formulario(self):
        self.assertContains(self.response, text='<form')
        self.assertContains(self.response, text='<input ', count=4)
        self.assertContains(self.response, text='method="post"')
        self.assertContains(self.response, text='csrfmiddlewaretoken')
        
        

class TestPaginaInicialComAutenticacao(TestCaseParaUsuarioLogado):  
        
    def test_valid(self):
        self.assertTrue(self.logged_in) 
               
    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')
        
        
        
class TestPostAutenticacao(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234qwer')
        self.response = self.client.post('/', {'username': 'testuser', 'password': '1234qwer'})    
               
    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')
        
        
        
class TestPaginaPrincipal(TestCaseParaUsuarioLogado):
    
    def test_formulario(self):        
        self.assertContains(self.response, text='csrfmiddlewaretoken')
        self.assertContains(self.response, text='<button', count=5)    
        self.assertContains(self.response, text='<input', count=5)
        self.assertContains(self.response, text='type="submit"', )
        self.assertContains(self.response, text=reverse('gerar_arquivo'), )
        
        
class TestGerarArquivo(TestCaseParaUsuarioLogado):
    
    def setUp(self):
        super(TestGerarArquivo, self).setUp()
        self.response = self.client.post(reverse('gerar_arquivo'), {'inicio': '18/10/2016', 'fim': '19/10/2016'}) 
         
    def test_ok(self):
        self.assertEqual(200, self.response.status_code)   
        self.assertTrue('Content-Disposition' in self.response) 
        self.assertTrue('18102016-19102016.txt' in self.response['Content-Disposition'], msg='Nome errado de arquivo' )
        
        
             
        
        

