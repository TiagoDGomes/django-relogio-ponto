# django-relogio-ponto
Sistema para gerenciamento de relógio de ponto

## Debug e testes
```sh
mkdir sistema_ponto
cd sistema_ponto
git clone https://github.com/TiagoDGomes/django-relogio-ponto.git
cd django-relogio-ponto
git submodule init
git submodule update
cd pyRelogioPonto
git fetch -v --progress "origin"
git pull -v --progress "origin" master
cd ..
virtualenv venv
cd venv
source bin/activate
cd ..
sudo apt-get install unixodbc-dev
pip install -r requirements.txt
cp settings.ini.default settings.ini
```

Edite o arquivo settings.ini:
```
[settings]
SECRET_KEY=UmaSequenciaDeCaracteresQualquer
DEBUG=True
ALLOWED_HOSTS=Endereco_do_Servidor
```

Crie uma senha de administrador:
```
python manage.py createsuperuser
```

Crie as tabelas da database:
```
python manage.py migrate
```

Execute o servidor:
```
python manage.py runserver 0.0.0.0:8000
```

Acesse o sistema:
http://Endereco_do_Servidor:8000/ponto
