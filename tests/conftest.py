def pytest_configure():
    from django.conf import settings

    settings.configure(
        ROOT_URLCONF='tests.project.urls',
        SECRET_KEY='not so secret',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'rest_framework',
            'tests.project'
        ],
    )
