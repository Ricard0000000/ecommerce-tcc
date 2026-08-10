"""
Django settings for config project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# 🚀 CARREGA AS VARIÁVEIS DO ARQUIVO .ENV
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SEGURANÇA
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-de-seguranca')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# 🚀 APPS
INSTALLED_APPS = [
    'jazzmin', # Mantido, pois você quer o visual dele
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'produtos',
    'accounts',
]

# ⚙ MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# 🧩 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'produtos.views.dados_carrinho', # 🛒 CARRINHO GLOBAL
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 🗄 DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# 🌍 TIME / LANGUAGE
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# 📁 STATIC & MEDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔐 LOGIN
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 🎨 JAZZMIN CONFIGURATION (Aqui está a chave para o visual)
JAZZMIN_SETTINGS = {
    "site_title": "Bonsai Garden Admin",
    "site_header": "Painel de Controle",
    "site_brand": "Bonsai Garden",
    "welcome_sign": "Bem-vindo ao sistema de gestão",
    "copyright": "Bonsai Garden TCC",
    "show_sidebar": True,
    "navigation_expanded": True,
    # Removi o custom_css temporariamente para evitar erro 404. 
    # Só adicione de volta se o arquivo existir fisicamente na pasta static/css/custom.css
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 💳/🚚 CONFIGURAÇÕES EXTERNAS
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
MELHOR_ENVIO_CLIENT_ID = os.getenv("MELHOR_ENVIO_CLIENT_ID")
MELHOR_ENVIO_CLIENT_SECRET = os.getenv("MELHOR_ENVIO_CLIENT_SECRET")
MELHOR_ENVIO_REDIRECT_URI = os.getenv("MELHOR_ENVIO_REDIRECT_URI")
CEP_ORIGEM = os.getenv("CEP_ORIGEM")
MELHOR_ENVIO_ACCESS_TOKEN = os.getenv("MELHOR_ENVIO_ACCESS_TOKEN")

# Configurações de Envio de E-mail (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '95ricard0.c0rrea@gmail.com'  # 👈 Seu e-mail do Gmail aqui
EMAIL_HOST_PASSWORD = 'kgxygheaqopgbmxq'  # 👈 A senha de 16 letras entra aqui, sem espaços
DEFAULT_FROM_EMAIL = 'Bonsai Garden <seu-email@gmail.com>'