from django.db.models import QuerySet
# from django.apps import apps


old_insert = QuerySet._insert


def _insert(self, objs, fields, return_id=False, raw=False, using=None):
    ret = old_insert(self, objs, fields, return_id, raw, using)
    try:
        self.model._tt_model
        print 'hooray, tt_model: %s' % self.model._tt_model
    except:
        print 'no tt_model: %s' % self.model
    return ret

_insert.alters_data = True
_insert.queryset_only = False


def patch_queryset():
    if hasattr(QuerySet, '_tt_patched'):
        return

    QuerySet._tt_patched = True
    QuerySet._insert = _insert
