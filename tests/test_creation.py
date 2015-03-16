import pytest


DJANGO_PROJECT = 'project1'
DJANGO_SETTINGS_MODULE = 'project1.settings'
DISABLE_MIGRATIONS = False
pytestmark = pytest.mark.usefixtures('setup_test_environment')


def test_transaction():
    from product.models import Product
    from django.db import transaction
    from django_timetravel import MAX, get_transaction_start_ts

    with transaction.atomic():
        ts = get_transaction_start_ts()

        p = Product(name='a', price=1)
        p.save()
        p.price = 2
        p.save()
        p.delete()

    p = Product(name='b', price=1)
    p.save()

    hist = Product._tt_model.objects.all()
    assert len(hist) == 3

    tran1 = [h for h in hist
             if h.tt_valid_from_ts == ts and h.tt_valid_until_ts == ts]

    assert len(tran1) == 2

    tran2 = [h for h in hist
             if h.tt_valid_from_ts > ts and h.tt_valid_until_ts == MAX]

    assert len(tran2) == 1
    assert tran2[0].name == 'b'
