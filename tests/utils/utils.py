import os
import re


def get_project_path(project_name):
    """Walks up in the path to find `pytest.ini`."""

    current = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(current, 'pytest.ini')):
            return os.path.join(current, project_name)
        current, _ = os.path.split(current)
        if not _:
            raise Exception('No `pytest.ini` found.')


def delete_migrations(project_name):
    project_path = get_project_path(project_name)
    for dirpath, dirnames, filenames in os.walk(project_path):
        if os.path.split(dirpath)[1] == 'migrations':
            for fn in [fn for fn in filenames if re.search('^\d{4}_', fn)]:
                to_delete = os.path.join(dirpath, fn)
                os.remove(to_delete)


def makemigrations(project_name):
    delete_migrations(project_name)
    from django.core.management import call_command
    call_command('makemigrations', interactive=False, verbosity=0)


def flush():
    from django.core.management import call_command
    call_command('flush', interactive=False, verbosity=0)
