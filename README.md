# Django Dummy Database

A fully-featured dummy database backend for Django that allows running all standard Django apps (admin, auth, contenttypes, etc.) without a real database.

## Features

- 🚀 Run Django with all standard apps - no database required
- 💾 In-memory storage - data persists during runtime
- 🔄 Full transaction support simulation
- 📊 Works with migrations - creates tables in memory
- 🎯 Compatible with Django 3.2+
- 🛡️ All database exceptions properly defined
- 🔧 No configuration changes needed - just swap the database backend

## Installation

```bash
pip install django-dummy-database
```

## Usage
Simply change your `DATABASES` setting in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_dummy_database',
        'NAME': 'dummy_db',
    }
}
```

That's it! You can keep all your standard Django apps:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # your apps...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## How It Works
The backend creates an in-memory storage that:
- Initializes all system tables (`django_content_type`, `auth_user`, etc.)
- Simulates SQL queries and returns appropriate results
- Maintains sequences for auto-increment fields
- Supports transactions, savepoints, and all standard database operations
- Handles migrations by creating tables in memory

## Use Cases
- **Development**: Work without setting up a real database
- **Testing**: Run tests faster without database overhead
- **CI/CD**: Simplify continuous integration pipelines
- **Demos**: Create portable demo applications
- **Static Sites**: Build Django sites that don't need persistent storage

## Requirements
- Python 3.8+
- Django 3.2+

## License
MIT License - see LICENSE file for details.


