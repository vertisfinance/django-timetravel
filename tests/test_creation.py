# import datetime

import pytest


DJANGO_PROJECT = 'test_projects/trading_system'
DJANGO_SETTINGS_MODULE = 'trading_system.settings'
DB_KEEP = True
pytestmark = pytest.mark.usefixtures('setup_test_environment')


# @pytest.mark.usefixtures('flush_after')
class TestCreation:
    def test_create_user(self, timestamps):
        """Create some users."""

        from django.contrib.auth.models import User

        timestamps.set(0)

        self.alice = User.objects.create_user('alice', password='alice')
        self.bob = User.objects.create_user('bob', password='bob')
        self.charlie = User.objects.create_user('charlie', password='charlie')

        timestamps.set(1)

        hist = User._tt_model.objects.all()
        assert len(hist) == 3

    def test_access_users(self, timestamps):
        from django.contrib.auth.models import User
        from django_timetravel import timetravel

        assert len(User.objects.all()) == 3

        with timetravel(timestamps.get(0)):
            assert len(User.objects.all()) == 0

        with timetravel(timestamps.get(1)):
            assert len(User.objects.all()) == 3

    def test_modify_user(self, timestamps):
        """Modify alice, but info does not disappear"""

        from django.contrib.auth.models import User
        from django_timetravel import timetravel, TimeTravelModelError

        alice = User.objects.get(username='alice')
        alice.email = 'alice@test.org'
        alice.save()

        timestamps.set(2)

        with timetravel(timestamps.get(1)):
            with pytest.raises(TimeTravelModelError):
                alice.email

            hist_alice = User.objects.get(username='alice')
            assert hist_alice.email == ''

        alice = User.objects.get(username='alice')
        assert alice.email == 'alice@test.org'

    def test_clients(self, timestamps):
        from client.models import Client
        from django_timetravel import timetravel

        client_a = Client(name='Corp A')
        client_b = Client(name='Corp B')

        Client.objects.bulk_create([client_a, client_b])

        timestamps.set(3)

        with timetravel(timestamps.get(2)):
            assert len(Client.objects.all()) == 0

        assert len(Client.objects.all()) == 2

        with timetravel(timestamps.get(3)):
            assert len(Client.objects.all()) == 2

        assert len(Client.objects.all()) == 2

    def test_bulk_update(self, timestamps):
        from client.models import Client
        from django_timetravel import timetravel

        assert len(Client.objects.filter(classification='A')) == 2
        assert len(Client.objects.filter(classification='B')) == 0

        Client.objects.all().update(classification='B')

        timestamps.set(4)

        with timetravel(timestamps.get(3)):
            assert len(Client.objects.filter(classification='A')) == 2
            assert len(Client.objects.filter(classification='B')) == 0

        with timetravel(timestamps.get(4)):
            assert len(Client.objects.filter(classification='A')) == 0
            assert len(Client.objects.filter(classification='B')) == 2

        assert len(Client.objects.filter(classification='A')) == 0
        assert len(Client.objects.filter(classification='B')) == 2

    def test_delete(self, timestamps):
        from product.models import Product
        from django_timetravel import timetravel, TimeTravelQuerySetError

        timestamps.set('before_create')

        Product.objects.bulk_create([Product(name='P1'),
                                     Product(name='P2'),
                                     Product(name='P3'),
                                     Product(name='P4')])

        timestamps.set('after_create')

        Product.objects.all().delete()

        timestamps.set('after_delete')

        with timetravel(timestamps.get('before_create')):
            assert len(Product.objects.all()) == 0

        with timetravel(timestamps.get('after_create')):
            qs = Product.objects.all()
            assert len(qs) == 4

        with timetravel(timestamps.get('after_delete')):
            assert len(Product.objects.all()) == 0

        with pytest.raises(TimeTravelQuerySetError):
            len(qs)

    def test_no_dbmod_in_tt(self):
        from product.models import Product
        from django_timetravel import (timetravel,
                                       TimeTravelDBModException,
                                       TimeTravelModelError)

        with timetravel(0):
            p = Product(name='P')
            with pytest.raises(TimeTravelDBModException):
                p.save()

            with pytest.raises(TimeTravelDBModException):
                Product.objects.all().delete()

            with pytest.raises(TimeTravelDBModException):
                Product.objects.update(name='X')

        with pytest.raises(TimeTravelModelError):
            p.name
