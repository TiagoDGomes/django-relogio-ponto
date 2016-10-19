from django.test import TestCase
from django.contrib.auth.models import User

class TestPaginaInicialSemAutenticar(TestCase):

    def setUp(self):
        self.response = self.client.get('/') 

    def test_200(self):
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'login.html')
    
    def test_formulario(self):
        self.assertContains(self.response, text='<form')
        self.assertContains(self.response, text='<input ', count=3)
        self.assertContains(self.response, text='method="post"')
        
        

class TestPaginaInicialComAutenticacao(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234qwer')
        self.logged_in = self.client.login(username=self.user.username, password='1234qwer')
        self.response = self.client.get('/', follow=True)    
        
    def test_valid(self):
        self.assertTrue(self.logged_in) 
               
    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')
        
        
        
class TestPaginaInicialAutenticando(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234qwer')
        self.response = self.client.post('/', {'username': 'testuser', 'password': '1234qwer'})    
               
    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')
        
             
        
        

