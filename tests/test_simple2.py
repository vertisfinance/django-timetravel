import pytest


DJANGO_PROJECT = 'project2'
DJANGO_SETTINGS_MODULE = 'project2.settings'
DISABLE_MIGRATIONS = False
pytestmark = pytest.mark.usefixtures('setup_test_environment')


def test_simple():
    from student.models import Student
    stud = Student(name='st1')
    stud.save()
