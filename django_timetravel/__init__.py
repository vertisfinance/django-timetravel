import threading
import time
import decimal


from django.db import connection


local = threading.local()
local.tran_ts = None
local.tt_ts = None


PK = 'tt_id'
OK = 'tt_orig_id'
CU = 'tt_create_modif_user_id'
DU = 'tt_delete_user_id'
VF = 'tt_valid_from_ts'
VU = 'tt_valid_until_ts'
FORBIDDEN_FIELDS = (PK, OK, CU, DU, VF, VU)


MAX = 999999999999
MIN = -MAX
Q = decimal.Decimal('.000001')


class TimeTravelModelError(Exception):
    """
    Error thrown when model instance is accessed outside of
    it's timetravel context.
    """
    def __init__(self, obj):
        actual_ctx = get_tt_ts()
        model_ctx = obj._tt_ts

        message = 'Using `%s` instance from %s in context %s'
        message = message % (obj._meta.model_name, model_ctx, actual_ctx)
        super(TimeTravelModelError, self).__init__(message)


class TimeTravelQuerySetError(Exception):
    """
    Error thrown when a queryset is accessed outside of
    it's timetravel context.
    """
    def __init__(self, obj):
        actual_ctx = get_tt_ts()
        qs_ctx = obj._tt_ts

        message = 'Using QuerySet from %s in context %s'
        message = message % (qs_ctx, actual_ctx)
        super(TimeTravelQuerySetError, self).__init__(message)


class TimeTravelDBModException(Exception):
    """
    Error thrown when save, update or delete is called in timetravel context.
    """
    def __init__(self):
        message = 'Saving or deleting in timetravel context is forbidden'
        super(TimeTravelDBModException, self).__init__(message)


def to_decimal(f):
    """Converts a float to decimal with precision given in global Q."""
    return decimal.Decimal(f).quantize(Q)


def get_transaction_start_ts():
    if connection.get_autocommit():
        return to_decimal(time.time())
    assert local.tran_ts is not None, 'This sould not be None...'
    return local.tran_ts


def set_transaction_start_ts():
    local.tran_ts = to_decimal(time.time())


def get_tt_ts():
    try:
        local.tt_ts
    except AttributeError:
        local.tt_ts = None
    return local.tt_ts


def set_tt_ts(ts):
    try:
        _ts = to_decimal(ts)
    except:
        raise Exception('Could not convert timetravel destination (%s) '
                        'to Decimal object.') % ts
    global local  # hmmm, funny
    local.tt_ts = _ts


def clear_tt_ts():
    global local
    local.tt_ts = None


def get_active_records(model, pks):
    return model._tt_model.objects.filter(**{OK + '__in': pks, VU: MAX})


def close_active_records(model, pks, ts):
    actives = get_active_records(model, pks)
    actives.update(**{VU: ts})


def create_history_record(model, obj, ts, pk=None, op=None):
    args = {VF: ts}

    fields = model._tt_model._meta.fields
    fields = [f for f in fields if hasattr(f, '_tt_field_attrname')]
    for field in fields:
        attr = getattr(obj, field._tt_field_attrname)
        is_pk = model._meta.get_field(field._tt_field_name).primary_key
        if is_pk and attr is None:
            attr = attr if attr is not None else pk
            assert attr is not None, 'No primary key'
        args[field.name] = attr

    return model._tt_model(**args)


def insert_history_records(model, history_objs):
    model._tt_model.objects.bulk_create(history_objs)


class timetravel(object):
    """The timetravel context manager."""
    def __init__(self, ts):
        self.tt_ts = ts

    def __enter__(self):
        set_tt_ts(self.tt_ts)

    def __exit__(self, type, value, traceback):
        clear_tt_ts()
