from django.db.models.deletion import Collector
from django.utils import six

from . import (close_active_records, get_transaction_start_ts,
               create_history_record, insert_history_records)


old_delete = Collector.delete


def delete(self):
    ts = get_transaction_start_ts()

    for qs in self.fast_deletes:
        pks = list(qs.values_list('pk', flat=True))
        close_active_records(qs.model, pks, ts)

    for model, objs in six.iteritems(self.data):
        pks = [o.pk for o in objs]
        close_active_records(model, pks, ts)

    old_delete(self)

    for model, instances_for_fieldvalues in six.iteritems(self.field_updates):
        sets = instances_for_fieldvalues.values()
        objs = set.union(*sets)
        pks = [o.pk for o in objs]
        close_active_records(model, pks, ts)
        history_objs = [create_history_record(model, o, ts, op='U')
                        for o in objs]
        insert_history_records(model, history_objs)


def patch_collector():
    if hasattr(Collector, '_tt_patched'):
        return
    Collector._tt_patched = True
    Collector.delete = delete
