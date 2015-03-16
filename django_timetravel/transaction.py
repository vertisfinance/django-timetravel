from django.db.backends import BaseDatabaseWrapper
from django.db.backends.sqlite3.base import DatabaseWrapper

from . import set_transaction_start_ts


old_set_autocommit = BaseDatabaseWrapper.set_autocommit


def set_autocommit(self, autocommit):
    old_set_autocommit(self, autocommit)
    if not autocommit:
        set_transaction_start_ts()


_old = DatabaseWrapper._start_transaction_under_autocommit


def _start_transaction_under_autocommit(self):
    _old(self)
    set_transaction_start_ts()


def patch_transaction():
    if not hasattr(BaseDatabaseWrapper, '_tt_patched'):
        BaseDatabaseWrapper._tt_patched = True
        BaseDatabaseWrapper.set_autocommit = set_autocommit

    if not hasattr(DatabaseWrapper, '_tt_patched_subclass'):
        DatabaseWrapper._tt_patched_subclass = True
        _new = _start_transaction_under_autocommit
        DatabaseWrapper._start_transaction_under_autocommit = _new
