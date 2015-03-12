import time

from django.db.models import QuerySet
# from django.apps import apps

from . import FORBIDDEN_FIELDS, MAX


PK = FORBIDDEN_FIELDS.get('pk')
OK = FORBIDDEN_FIELDS.get('ok')
CU = FORBIDDEN_FIELDS.get('cu')
DU = FORBIDDEN_FIELDS.get('du')
VF = FORBIDDEN_FIELDS.get('vf')
VU = FORBIDDEN_FIELDS.get('vu')


def get_active_record(model, obj):
    tt_model = model._tt_model
    return tt_model.objects.get(**{OK: obj.pk, VU: MAX})


def close_active_record(model, obj):
    active = get_active_record(model, obj)
    setattr(active, VU, time.time())
    active.save()


def insert_history_record(model, obj, pk=None):
    tt_model = model._tt_model

    args = {CU: None,  # TODO
            VF: time.time()}

    fields = tt_model._meta.fields
    fields = [f for f in fields if hasattr(f, '_tt_field_attrname')]
    for field in fields:
        attr = getattr(obj, field._tt_field_attrname)
        is_pk = model._meta.get_field(field._tt_field_name).primary_key
        if is_pk and attr is None:
            attr = attr if attr is not None else pk
            assert attr is not None, 'No primary key'
        args[field.name] = attr

    model_instance = tt_model(**args)
    model_instance.save()


###
old__insert = QuerySet._insert


def _insert(self, objs, fields, return_id=False, raw=False, using=None):
    if hasattr(self.model, '_tt_model'):
        # Must not allow multiple objs in _insert, or else we have no way to
        # retrieve the pk of newly inserted rows
        if len(objs) > 1:
            for obj in objs:
                self._insert([obj], fields, return_id=True,
                             raw=raw, using=using)
            return
        else:
            ret = old__insert(self, objs, fields, return_id=True,
                              raw=raw, using=using)
            obj = objs[0]
            insert_history_record(self.model, obj, pk=ret)

            return ret
    else:
        return old__insert(self, objs, fields, return_id, raw, using)


_insert.alters_data = True
_insert.queryset_only = False


###
old__update = QuerySet._update


def _update(self, values):
    ret = old__update(self, values)

    if hasattr(self.model, '_tt_model'):
        for obj in self:
            close_active_record(self.model, obj)
            insert_history_record(self.model, obj)

    return ret


_update.alters_data = True
_update.queryset_only = False


###
old_update = QuerySet._update


def update(self, **kwargs):
    ret = old_update(self, **kwargs)

    if hasattr(self.model, '_tt_model'):
        for obj in self:
            close_active_record(self.model, obj)
            insert_history_record(self.model, obj)

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
