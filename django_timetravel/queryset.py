from django.db.models import QuerySet

from . import (create_history_record,
               close_active_records,
               insert_history_records,
               get_transaction_start_ts)


###
old__insert = QuerySet._insert


def _insert(self, objs, fields, return_id=False,
            raw=False, using=None):
    if hasattr(self.model, '_tt_model'):
        # Must not allow multiple objs in _insert, or else we have no way to
        # retrieve the pk of newly inserted rows
        # TODO: Warning
        history_objs = []
        for obj in objs:
            pk = old__insert(self, [obj], fields, return_id=True,
                             raw=raw, using=using)
            ts = get_transaction_start_ts()
            ho = create_history_record(self.model, obj, ts, pk=pk, op='I')
            history_objs.append(ho)
        insert_history_records(self.model, history_objs)
        return pk if len(objs) == 1 else None
    else:
        return old__insert(self, objs, fields, return_id, raw, using)


_insert.alters_data = True
_insert.queryset_only = False


###
#  This is only used in models.base...
old__update = QuerySet._update


def _update(self, values):
    tt_needed = hasattr(self.model, '_tt_model')

    if not tt_needed:
        return old__update(self, values)

    ts = get_transaction_start_ts()

    pks = list(self.values_list('pk', flat=True))
    close_active_records(self.model, pks, ts)

    ret = old__update(self, values)

    # No need to do the same hack as in `update` below, no pk's updated
    pk_name = self.model._meta.pk.name
    objs = self.model._base_manager.filter(**{pk_name + '__in': pks})
    history_objs = [create_history_record(self.model, o, ts, op='U')
                    for o in objs]
    insert_history_records(self.model, history_objs)

    return ret


_update.alters_data = True
_update.queryset_only = False


###
old_update = QuerySet.update


def update(self, **kwargs):
    tt_needed = hasattr(self.model, '_tt_model')

    if not tt_needed:
        return old_update(self, **kwargs)

    ts = get_transaction_start_ts()

    pks = list(self.values_list('pk', flat=True))
    close_active_records(self.model, pks, ts)

    ret = old_update(self, **kwargs)

    pk_name = self.model._meta.pk.name
    if pk_name in kwargs:
        new_pk_value = kwargs.get(pk_name)
        obj = self.model._base_manager.get(**{pk_name: new_pk_value})
        history_objs = [create_history_record(self.model, obj, ts, op='U')]
    else:
        objs = self.model._base_manager.filter(**{pk_name + '__in': pks})
        history_objs = [create_history_record(self.model, o, ts, op='U')
                        for o in objs]
    insert_history_records(self.model, history_objs)

    return ret


update.alters_data = True


###
def patch_queryset():
    if hasattr(QuerySet, '_tt_patched'):
        return
    QuerySet._tt_patched = True
    QuerySet._insert = _insert
    QuerySet._update = _update
    QuerySet.update = update
