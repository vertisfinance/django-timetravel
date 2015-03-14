# -*- coding: utf-8 -*-

import os
import sys

import pytest
from pytest_django.plugin import django_settings_is_configured, _setup_django

from .utils.utils import get_project_path


@pytest.fixture(autouse=True, scope='session')
def django_test_environment(request):
    """
    copied from pytest-django
    """
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
    sys.path.insert(0, get_project_path('test_project'))
    _setup_django()
    if django_settings_is_configured():
        from django.conf import settings
        from pytest_django.compat import (setup_test_environment,
                                          teardown_test_environment)
        from pytest_django.compat import setup_databases, teardown_databases
        settings.DEBUG = False
        setup_test_environment()
        db_cfg = setup_databases(verbosity=0, interactive=False)
        request.addfinalizer(teardown_test_environment)

        def teardown_database():
            teardown_databases(db_cfg)

        request.addfinalizer(teardown_database)
