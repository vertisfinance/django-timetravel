import threading
import time
import decimal


from django.db import connection


local = threading.local()
local.tran_ts = None
local.tt_ts = None


FORBIDDEN_FIELDS = {'pk': 'tt_id',
                    'ok': 'tt_orig_id',
                    'cu': 'tt_create_modif_user_id',
                    'du': 'tt_delete_user_id',
                    'vf': 'tt_valid_from_ts',
                    'vu': 'tt_valid_until_ts'}

PK = FORBIDDEN_FIELDS.get('pk')
OK = FORBIDDEN_FIELDS.get('ok')
CU = FORBIDDEN_FIELDS.get('cu')
DU = FORBIDDEN_FIELDS.get('du')
VF = FORBIDDEN_FIELDS.get('vf')
VU = FORBIDDEN_FIELDS.get('vu')

MAX = 999999999999
Q = decimal.Decimal('.000001')


def to_decimal(f):
    return decimal.Decimal(f).quantize(Q)


def get_transaction_start_ts():
    if connection.get_autocommit():
        return to_decimal(time.time())
    assert local.tran_ts is not None, 'This sould not be None...'
    return local.tran_ts


def set_transaction_start_ts():
    local.tran_ts = to_decimal(time.time())


def get_tt_ts():
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
