import dj_database_url
import os
from settings.common import *

#==============================================================================
# Generic Django Project Settings
#==============================================================================

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.config()
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com', '.rashirt.me']

# Make this unique, and don't share it with anybody.
# Set it by issuing following command
# <code>
# heroku config:add SECRET_KEY=''
# </code>
SECRET_KEY = os.environ['SECRET_KEY']

#==============================================================================
# SSL Processing
#==============================================================================

# If this is set to True, the cookie will be marked as 'secure,' which means
# browsers may ensure that the cookie is only sent under an HTTPS connection.
SESSION_COOKIE_SECURE = True

# If this is set to True, the cookie will be marked as 'secure' which means
# browsers may ensure that the cookie is only sent under an HTTPS connection.
CSRF_COOKIE_SECURE = True

# See https://docs.djangoproject.com/en/1.6/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Whether to expire the session when the user closes his or her browser. See
# https://docs.djangoproject.com/en/1.6/topics/http/sessions/#browser-length-vs-persistent-sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#==============================================================================
# Payment Processing
#==============================================================================

# Set it by issuing following command
# <code>
# heroku config:add STRIPE_PUBLISHABLE_KEY=''
# </code>
STRIPE_PUBLIC_KEY = os.environ['STRIPE_PUBLIC_KEY']

# Set it by issuing following command
# <code>
# heroku config:add STRIPE_API_KEY=''
# </code>
STRIPE_PRIVATE_KEY = os.environ['STRIPE_PRIVATE_KEY']

#==============================================================================
# Email Support w/ Heroku & Mandrill
#==============================================================================

INSTALLED_APPS += (
    'djrill',
)

# Set it by issuing following command
# <code>
# heroku config:add MANDRILL_API_KEY=''
# </code>
MANDRILL_API_KEY = os.environ['MANDRILL_APIKEY']

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

#==============================================================================
# Static Files Support w/ Amazon S3
#==============================================================================

INSTALLED_APPS += (
    'storages',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Your Amazon Web Services storage bucket name, as a string.
# Set it by issuing following command
# <code>
# heroku config:add AWS_ACCESS_KEY_ID=''
# </code>
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

# Your Amazon Web Services access key, as a string.
# Set it by issuing following command
# <code>
# heroku config:add AWS_ACCESS_KEY_ID=''
# </code>
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

# Your Amazon Web Services secret access key, as a string.
# Set it by issuing following command
# <code>
# heroku config:add AWS_SECRET_ACCESS_KEY=''
# </code>
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

AWS_QUERYSTRING_AUTH = False

from boto.s3.connection import SubdomainCallingFormat
AWS_CALLING_FORMAT = SubdomainCallingFormat

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
