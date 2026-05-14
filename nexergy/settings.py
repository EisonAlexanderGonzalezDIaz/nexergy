"""
nexergy/settings.py
Configuración principal del proyecto NEXERGY.
Django 4.2 + MySQL 8.0
"""

from pathlib import Path
from decouple import config   # lee variables del archivo .env

# ── Rutas ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Seguridad ─────────────────────────────────────────────
# La SECRET_KEY viene del .env, nunca queda expuesta en el código
SECRET_KEY = config('SECRET_KEY', default='clave-insegura-solo-para-desarrollo')

# DEBUG = True en desarrollo, False en producción
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

# ── Apps instaladas ───────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps de NEXERGY
    'accounts',
    'entidades',
    'consumos',
    'calculadora',
    'dashboard',
    'recomendaciones',
    'reportes',
]

# ── Middleware ────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # protección CSRF activa
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nexergy.urls'

# ── Templates ─────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django buscará templates en la carpeta /templates/ de la raíz
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nexergy.wsgi.application'

# ── Base de datos MySQL ───────────────────────────────────
# Las credenciales se leen del archivo .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     config('DB_NAME',     default='nexergy_db'),
        'USER':     config('DB_USER',     default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST':     config('DB_HOST',     default='localhost'),
        'PORT':     config('DB_PORT',     default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',   # soporte completo de Unicode
        },
    }
}

# ── Validaciones de contraseña ────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Localización ──────────────────────────────────────────
LANGUAGE_CODE = 'es-co'    # español Colombia
TIME_ZONE     = 'America/Bogota'
USE_I18N      = True
USE_TZ        = True

# ── Archivos estáticos (CSS, JS, imágenes) ────────────────
STATIC_URL  = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ── Sesiones ──────────────────────────────────────────────
# Cierra sesión tras 30 min de inactividad
SESSION_COOKIE_AGE    = 1800
SESSION_SAVE_EVERY_REQUEST = True

# ── Redirecciones de autenticación ───────────────────────
LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Archivos estáticos en producción ──────────
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'