from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    integrations=[DjangoIntegration()]  
)

ALLOWED_HOSTS = [
    'agphr.com',
    'www.agphr.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://agphr.com',
    'https://www.agphr.com',
]
DEBUG=False
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

STATIC_ROOT = '/home/prakara/agppay/public_html/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/prakara/agppay/public_html/media/'
