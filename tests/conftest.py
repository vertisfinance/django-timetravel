# -*- coding: utf-8 -*-

import os
import sys

import pytest
from pytest_django.plugin import _setup_django
from pytest_django.migrations import DisableMigrations

from .utils import utils


modules_not_to_delete = None


@pytest.fixture(scope='module')
def setup_test_environment(request):
    """
    We destroy the test database and reload django entirely with a
    (possibly) different project. Also deletes and recreates migration files.
    """
    global modules_not_to_delete

    DJANGO_SETTINGS_MODULE = request.module.DJANGO_SETTINGS_MODULE
    DJANGO_PROJECT = request.module.DJANGO_PROJECT
    DJANGO_PROJECT_PATH = utils.get_project_path(DJANGO_PROJECT)

    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

    orig_path = sys.path[:]
    sys.path.insert(0, DJANGO_PROJECT_PATH)

    if not modules_not_to_delete:
        modules_not_to_delete = sys.modules.keys()
    else:
        for module in sys.modules.keys():
            if module not in modules_not_to_delete:
                del sys.modules[module]

    _setup_django()

    from django.conf import settings

    settings.DEBUG = False
    if request.module.DISABLE_MIGRATIONS:
        settings.MIGRATION_MODULES = DisableMigrations()
    else:
        utils.makemigrations(DJANGO_PROJECT)

    from pytest_django.compat import (setup_test_environment,
                                      teardown_test_environment,
                                      setup_databases,
                                      teardown_databases)

    setup_test_environment()
    db_cfg = setup_databases(verbosity=0, interactive=False)

    def teardown():
        teardown_test_environment
        teardown_databases(db_cfg)
        sys.path = orig_path

    request.addfinalizer(teardown)


@pytest.fixture()
def flush(request):
    def teardown():
        utils.flush()

    request.addfinalizer(teardown)
