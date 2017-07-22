from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from kkb.process import get_context,postlink_process as postlink
version_info = (0, 3, 0)

__version__ = version = '.'.join(map(str, version_info))
__project__ = PROJECT = 'kkb'
__author__ = AUTHOR = "sofaku <kushibayev@gmail.com>"

if not hasattr(settings, 'MERCHANT_ID'):
	raise ImproperlyConfigured('MERCHANT_ID is required')

if not hasattr(settings, 'MERCHANT_CERTIFICATE_ID'):
	raise ImproperlyConfigured('MERCHANT_CERTIFICATE_ID is required')

if not hasattr(settings, 'MERCHANT_NAME'):
	raise ImproperlyConfigured('MERCHANT_NAME is required')

if not hasattr(settings, 'PRIVATE_KEY_FN'):
	raise ImproperlyConfigured('PRIVATE_KEY_FN is required')

if not hasattr(settings, 'PRIVATE_KEY_PASS'):
	raise ImproperlyConfigured('PRIVATE_KEY_PASS is required')

if not hasattr(settings, 'PUBLIC_KEY_FN'):
	raise ImproperlyConfigured('PUBLIC_KEY_FN is required')


settings.XML_TEMPLATE_FN = getattr(settings, 'XML_TEMPLATE_FN', 'kkb/template.xml')

settings.XML_COMMAND_TEMPLATE_FN = getattr(settings, 'XML_COMMAND_TEMPLATE_FN', 'kkb/command_template.xml')