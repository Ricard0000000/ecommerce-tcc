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
        'DIRS': [BASE_DIR / 'templates'], # 👈 Ponto chave: instrui o Django a procurar primeiro na sua pasta templates/
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'produtos.views.dados_carrinho',
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
STATIC_ROOT = BASE_DIR / "staticfiles"
# Usamos CompressedStaticFilesStorage para evitar falhas caso falte algum mapa de estáticos
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
WHITENOISE_ROOT = MEDIA_ROOT
WHITENOISE_INDEX_FILE = True

# 🔐 LOGIN
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 🎨 JAZZMIN CONFIGURATION
JAZZMIN_SETTINGS = {
    "site_title": "Bonsai Garden Admin",
    "site_header": "Painel de Controle",
    "site_brand": "Bonsai Garden",
    "site_url": "/admin/",
    "index_url": "/admin/",
    "welcome_sign": "Bem-vindo ao sistema de gestão",
    "copyright": "Bonsai Garden TCC",
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False,
    "topmenu_links": [],
    "usermenu_links": [],
    "custom_css": None,
    "custom_js": None,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "theme": "default",
    "default_theme_mode": "light",
    "sidebar_nav_child_indent": False,
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
EMAIL_HOST_USER = '95ricard0.c0rrea@gmail.com'
EMAIL_HOST_PASSWORD = 'kgxygheaqopgbmxq'
DEFAULT_FROM_EMAIL = 'Bonsai Garden <95ricard0.c0rrea@gmail.com>'