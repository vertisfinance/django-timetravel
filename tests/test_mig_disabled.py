import pytest


DJANGO_PROJECT = 'project2'
DJANGO_SETTINGS_MODULE = 'project2.settings'
DISABLE_MIGRATIONS = False
pytestmark = pytest.mark.usefixtures('setup_test_environment')


def test_tables_exist():
    """Test this by simply insert."""
    from student.models import Student
    s = Student(name='John Doe')
    s.save()
    assert s.pk
