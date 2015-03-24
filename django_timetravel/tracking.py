from django.db.models import QuerySet
from django.db.models.deletion import Collector
from django.utils import six

from . import (create_history_record,
               close_active_records,
               insert_history_records,
               get_transaction_start_ts,
               TimeTravelDBModException,
               get_tt_ts)


###
old__insert = QuerySet._insert


def _insert(self, objs, fields, return_id=False,
            raw=False, using=None):
    if get_tt_ts() is not None:
        raise TimeTravelDBModException()

    tt_needed = hasattr(self.model, '_tt_model')
    if not tt_needed:
        return old__insert(self, objs, fields, return_id, raw, using)

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


_insert.alters_data = True
_insert.queryset_only = False


###
#  This is only used in models.base...
old__update = QuerySet._update


def _update(self, values):
    if get_tt_ts() is not None:
        raise TimeTravelDBModException()

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
    if get_tt_ts() is not None:
        raise TimeTravelDBModException()

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
old_delete = Collector.delete


def delete(self):
    if get_tt_ts() is not None:
        raise TimeTravelDBModException()

    ts = get_transaction_start_ts()

    for qs in self.fast_deletes:
        pks = list(qs.values_list('pk', flat=True))
        if hasattr(qs.model, '_tt_model'):
            close_active_records(qs.model, pks, ts)

    for model, objs in six.iteritems(self.data):
        pks = [o.pk for o in objs]
        if hasattr(model, '_tt_model'):
            close_active_records(model, pks, ts)

    old_delete(self)

    for model, instances_for_fieldvalues in six.iteritems(self.field_updates):
        sets = instances_for_fieldvalues.values()
        objs = set.union(*sets)
        pks = [o.pk for o in objs]
        if hasattr(model, '_tt_model'):
            close_active_records(model, pks, ts)
            history_objs = [create_history_record(model, o, ts, op='U')
                            for o in objs]
            insert_history_records(model, history_objs)


def patch_tracking():
    if not hasattr(Collector, '_tt_tracking_patched'):
        Collector._tt_patched = True
        Collector.delete = delete

    if not hasattr(QuerySet, '_tt_tracking_patched'):
        QuerySet._tt_patched = True
        QuerySet._insert = _insert
        QuerySet._update = _update
        QuerySet.update = update
