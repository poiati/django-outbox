=============
Django Outbox
=============

Django Outbox is an app that enable you to see the emails sent by your project through the web browser.

It capture all mails and show in a simple web interface.

Quick Start
-----------

Install the package in your environment::

  $ pip install django-outbox

Configure your django development settings file to use file based email backend::

  from os import path

  EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
  EMAIL_FILE_PATH = path.join(ROOT_PATH, 'tmp', 'app-mails')

Also add django_outbox to your installed apps::

  INSTALLED_APPS += (
    django_outbox,
  )

Add the django outbox url to your urls.py::

  # urls.py
  from django.conf import settings

  # This will prevent from showing the outbox in production. The outbox
  # will only be available when the DEBUG setting is true.
  if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^outbox/', include('django_outbox.urls')),
    ) 

Now just run your application in **debug** mode and access */outbox*. All should be working!
