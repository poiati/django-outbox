Django Outbox
=============

![Downloads](https://img.shields.io/pypi/dm/django-outbox.svg?style=flat)
[![Code Health](https://landscape.io/github/poiati/django-outbox/master/landscape.svg?style=flat)](https://landscape.io/github/poiati/django-outbox/master)
![Versions](https://pypip.in/py_versions/django-outbox/badge.svg?style=flat)

Capture all mails sent and show it in a simple web interface.

Quick Start
-----------

Install the package in your environment:

```sh
$ pip install django-outbox
```

Configure your django development settings file to use file based email backend:

```python
from os import path

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = path.join(ROOT_PATH, 'tmp', 'app-mails')
```

Also add django_outbox to your installed apps:

```python

  INSTALLED_APPS += (
    'django_outbox',
  )
```

Add the django outbox url to your urls.py:

```python
  # urls.py
  from django.conf import settings

  # This will prevent from showing the outbox in production. The outbox
  # will only be available when the DEBUG setting is true.
  if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^outbox/', include('django_outbox.urls')),
    ) 
```

Now just run your application in **debug** mode and access */outbox*. All should be working!

Contributing
------------

This project use pytest_. To run the tests just type:
  
```bash
  $ py.test
```
