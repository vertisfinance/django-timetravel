# -*- coding: utf-8 -*-

import os
import sys
import time

import pytest
from pytest_django.plugin import _setup_django
from pytest_django.migrations import DisableMigrations

from . import (get_project_path, makemigrations,
               delete_migrations, flush as flush_db)


modules_not_to_delete = None


@pytest.fixture(scope='module')
def setup_test_environment(request):
    """
    Sets up a django test environment, makes migration files (deletes
    existing ones first), creates test database and applies migrations.
    At the end database is destroyed, migration files are deleted.

    It is not easy to run two different django apps in one process, even if
    we do it one after the other. Most modules need to be reimported, which
    involves some hacking :(.

    Modules must define:
        - `DJANGO_SETTINGS_MODULE`: will set the environment variable
        - `DJANGO_PROJECT`: path to the project main directory relative to
                            `pytest.ini`
    Optional:
        - `DISABLE_MIGRATIONS`: When set to `True`, test db creation will not
                                use the migration machinery.
    """
    global modules_not_to_delete

    settings_module = request.module.DJANGO_SETTINGS_MODULE
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    project_path = get_project_path(request.module.DJANGO_PROJECT)
    orig_path = sys.path[:]
    sys.path.insert(0, project_path)

    if not modules_not_to_delete:
        modules_not_to_delete = sys.modules.keys()
    else:
        for module in sys.modules.keys():
            if module not in modules_not_to_delete:
                del sys.modules[module]

    _setup_django()

    from django.conf import settings

    settings.DEBUG = False

    if getattr(request.module, 'DISABLE_MIGRATIONS', False):
        settings.MIGRATION_MODULES = DisableMigrations()
    else:
        makemigrations(project_path)

    from pytest_django.compat import (setup_test_environment,
                                      teardown_test_environment,
                                      setup_databases,
                                      teardown_databases)

    setup_test_environment()
    db_cfg = setup_databases(verbosity=0, interactive=False)

    def teardown():
        db_keep = getattr(request.module, 'DB_KEEP', False)
        if not db_keep:
            teardown_databases(db_cfg)
        teardown_test_environment()
        sys.path = orig_path
        delete_migrations(project_path)

    request.addfinalizer(teardown)


@pytest.fixture(scope='class')
def flush_after(request):
    def teardown():
        flush_db()

    request.addfinalizer(teardown)


class Timestamps:
    ts = {}

    def set(self, name):
        from django_timetravel import to_decimal
        self.ts[name] = to_decimal(time.time())

    def get(self, name):
        return self.ts[name]


@pytest.fixture(scope='class')
def timestamps():
    return Timestamps()
