import pytest


DJANGO_PROJECT = 'test_projects/trading_system'
DJANGO_SETTINGS_MODULE = 'trading_system.settings'
pytestmark = pytest.mark.usefixtures('setup_test_environment')


@pytest.mark.usefixtures('flush')
class TestCreation:
    def test_create_user(self):
        from django.contrib.auth.models import User

        alice = User.objects.create_user('alice', password='alice')
        alice.email = 'alice@test.com'
        alice.save()

        hist = User._tt_model.objects.all()
        assert len(hist) == 2
