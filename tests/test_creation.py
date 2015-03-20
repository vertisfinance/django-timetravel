import datetime

import pytest


DJANGO_PROJECT = 'test_projects/trading_system'
DJANGO_SETTINGS_MODULE = 'trading_system.settings'
DB_KEEP = True
pytestmark = pytest.mark.usefixtures('setup_test_environment')


def create_simple_setup():
    from client.models import Client, Clearer, Contract
    from product.models import Product, Forward, Futures

    p = Product(name='STOCK')
    p.save()

    cl = Clearer(name='Clearer Ltd.')
    cl.save()

    fut = Futures(name='STOCK_FWD',
                  underlying=p,
                  expiry=datetime.date(2015, 12, 15),
                  clearer=cl)
    fut.save()


@pytest.mark.usefixtures('flush_after')
class TestCreation:
    def test_create_user(self):
        from django.contrib.auth.models import User

        alice = User.objects.create_user('alice', password='alice')
        alice.email = 'alice@test.com'
        alice.save()

        hist = User._tt_model.objects.all()
        assert len(hist) == 2

    def test_simple(self):
        create_simple_setup()
