import time

from django.db.models import QuerySet
# from django.apps import apps

from . import FORBIDDEN_FIELDS


PK = FORBIDDEN_FIELDS.get('pk')
CU = FORBIDDEN_FIELDS.get('cu')
DU = FORBIDDEN_FIELDS.get('du')
VF = FORBIDDEN_FIELDS.get('vf')
VU = FORBIDDEN_FIELDS.get('vu')


# def insert_history_records(model, objs):
#     if hasattr(model, '_tt_model'):
#         tt_model = model._tt_model

#         _objs = []

#         for obj in objs:
#             args = {
#                 CU: None,  # TODO
#                 VF: time.time()}

#             fields = tt_model._meta.fields
#             fields = [f for f in fields if hasattr(f, '_tt_copy_attrname')]
#             for field in fields:
#                 attr_name = field._tt_copy_attrname
#                 attr = getattr(obj, attr_name)
#                 is_pk = model._meta.get_field(attr_name).primary_key
#                 if is_pk and attr is None:
#                     attr = ret
#                 args[field.name] = attr
#             _objs.append(tt_model(**args))

#         tt_model.objects.bulk_create(_objs)

###
old__insert = QuerySet._insert


def _insert(self, objs, fields, return_id=False, raw=False, using=None):
    ret = old__insert(self, objs, fields, return_id, raw, using)
    print ret

    if hasattr(self.model, '_tt_model'):
        tt_model = self.model._tt_model

        _objs = []

        for obj in objs:
            args = {
                CU: None,  # TODO
                VF: time.time()}

            fields = tt_model._meta.fields
            fields = [f for f in fields if hasattr(f, '_tt_copy_attrname')]
            for field in fields:
                attr_name = field._tt_copy_attrname
                attr = getattr(obj, attr_name)
                is_pk = self.model._meta.get_field(attr_name).primary_key
                if is_pk and attr is None:
                    attr = ret
                args[field.name] = attr
            _objs.append(tt_model(**args))

        tt_model.objects.bulk_create(_objs)

    return ret
_insert.alters_data = True
_insert.queryset_only = False


###
old__update = QuerySet._update


def _update(self, values):
    ret = old__update(self, values)

    if hasattr(self.model, '_tt_model'):
        tt_model = self.model._tt_model

        _objs = []

        for obj in self:
            args = {
                CU: None,  # TODO
                VF: time.time()}

            fields = tt_model._meta.fields
            fields = [f for f in fields if hasattr(f, '_tt_copy_attrname')]
            for field in fields:
                attr_name = field._tt_copy_attrname
                attr = getattr(obj, attr_name)
                is_pk = self.model._meta.get_field(attr_name).primary_key
                if is_pk and attr is None:
                    attr = ret
                args[field.name] = attr
            _objs.append(tt_model(**args))

        tt_model.objects.bulk_create(_objs)

    return ret
_update.alters_data = True
_update.queryset_only = False


###
old_update = QuerySet._update


def update(self, **kwargs):
    ret = old_update(self, **kwargs)
    for obj in self:
        print obj
    return ret
update.alters_data = True


###
def patch_queryset():
    if hasattr(QuerySet, '_tt_patched'):
        return
    # QuerySet._tt_patched = True
    # QuerySet._insert = _insert
    # QuerySet._update = _update
    # QuerySet.update = update
