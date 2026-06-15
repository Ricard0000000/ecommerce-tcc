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

# 🔐 SEGURANÇA: Chaves vindas do arquivo .env
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-de-seguranca')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Liberado para aceitar o domínio da Render quando fizermos o deploy
ALLOWED_HOSTS = ['*']


# 🚀 APPS
INSTALLED_APPS = [
    'jazzmin',

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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 📁 Essencial para os estáticos na nuvem
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

                # 🛒 CARRINHO GLOBAL
                'produtos.views.dados_carrinho',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# 🗄 DATABASE (Híbrido: PostgreSQL na Nuvem / SQLite Local)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Se a nuvem fornecer uma URL de banco de dados (PostgreSQL), o Django usa ela automaticamente
if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# 🔐 VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 🌍 TIME / LANGUAGE
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# 📁 STATIC & WHITENOISE
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Otimização para o WhiteNoise compactar os arquivos estáticos do Jazzmin
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# 📸 MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 🔐 LOGIN
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# 🎨 JAZZMIN
JAZZMIN_SETTINGS = {
    "site_title": "Bonsai Garden Admin",
    "site_header": "Painel de Controle",
    "site_brand": "Bonsai Garden",
    "welcome_sign": "Bem-vindo ao sistema de gestão",
    "copyright": "Bonsai Garden TCC",

    "show_sidebar": True,
    "navigation_expanded": True,

    "custom_css": "css/custom.css",
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 💳 CONFIGURAÇÕES MERCADO PAGO
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")


# 🚚 CONFIGURAÇÕES MELHOR ENVIO
MELHOR_ENVIO_CLIENT_ID = os.getenv("MELHOR_ENVIO_CLIENT_ID")
MELHOR_ENVIO_CLIENT_SECRET = os.getenv("MELHOR_ENVIO_CLIENT_SECRET")
MELHOR_ENVIO_REDIRECT_URI = os.getenv("MELHOR_ENVIO_REDIRECT_URI")
CEP_ORIGEM = os.getenv("CEP_ORIGEM")