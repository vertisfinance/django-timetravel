from django.db.models.options import Options

from . import get_tt_ts


class DBTableDescriptor(object):
    def __get__(self, instance, owner):
        if hasattr(instance, '_tt_model') and get_tt_ts():
            return instance._tt_model._meta.db_table
        else:
            if not hasattr(instance, '_tt_db_table'):
                instance._tt_db_table = instance.__dict__['db_table']

            return instance._tt_db_table

    def __set__(self, instance, value):
        instance._tt_db_table = value


def patch_options():
    if not hasattr(Options, '_tt_patched'):
        Options._tt_patched = True
        Options.db_table = DBTableDescriptor()
