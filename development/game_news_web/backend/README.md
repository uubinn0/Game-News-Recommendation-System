# backend

## Set Django 

### Install Django
```
pip install django
```
### Verify Django Installation
```
django-admin --version
```

### Create a New Django Project
```
django-admin startproject myproject
cd myproject
```
### Run the Development Server
```
python manage.py runserver (url):(p


## Issue : Allowed Hosts Problem in Django

When deploying a Django application, a 403 Forbidden error occurs due to incorrect `ALLOWED_HOSTS` settings. This error happens when Django checks the `Host` header of the request and blocks access from unapproved hosts.

## Solution

1. Open the `settings.py` file and locate the `ALLOWED_HOSTS` setting.
2. Set `ALLOWED_HOSTS` to `['*']` to allow access from all hosts.
   ```python
   ALLOWED_HOSTS = ['*']