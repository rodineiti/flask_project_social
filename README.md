# flask_project_social
Rede Social simples com Microframework Flask em Python

# Setar as credenciais do pusher e email

--Em config.py - adicionar suas credenciais:

--PUSHER_APP_ID = ''
--PUSHER_KEY = ''
--PUSHER_SECRET = ''
--PUSHER_CLUSTER = 'us2'
--PUSHER_SSL = True

--MAIL_SERVER = ''
--MAIL_PORT = 465
--MAIL_USERNAME = ''
--MAIL_PASSWORD = ''
--MAIL_USE_TLS = False
--MAIL_USE_SSL = True

# Comandos - testado no linux - em um ambiente online gitpod.io

1 - Instalar o pip
2 - Instalar virtualenv
3 - Criar uma virtualenv: virtualenv -p python3 venv
4 - Ativar a venv criada: . venv/bin/active
5 - Rodar: export PIP_USER=no
6 - Instalar as dependências do projeto: venv/bin/pip3 install -r requirements.txt
7 - Rodar o projeto: python3 run.py runserver

