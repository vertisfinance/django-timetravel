from django.db.models import Model, QuerySet

from . import get_tt_ts


class TimeTravelModelError(Exception):
    def __init__(self, obj):
        actual_ctx = get_tt_ts()
        model_ctx = obj._tt_ts

        message = 'Using `%s` instance from %s in context %s'
        message = message % (obj._meta.model_name, model_ctx, actual_ctx)
        super(TimeTravelModelError, self).__init__(message)


class TimeTravelQuerySetError(Exception):
    def __init__(self, obj):
        actual_ctx = get_tt_ts()
        qs_ctx = obj._tt_ts

        message = 'Using QuerySet from %s in context %s'
        message = message % (qs_ctx, actual_ctx)
        super(TimeTravelQuerySetError, self).__init__(message)


old___getattribute__ = Model.__getattribute__


def __getattribute__model(self, name):
    if name == '_meta':
        return old___getattribute__(self, '_meta')

    if name == '_tt_ts':
        try:
            return old___getattribute__(self, '_tt_ts')
        except AttributeError:
            return None

    if get_tt_ts() != self._tt_ts:
        raise TimeTravelModelError(self)

    return old___getattribute__(self, name)


old___init__ = Model.__init__


def __init__model(self, *args, **kwargs):
    self._tt_ts = get_tt_ts()
    old___init__(self, *args, **kwargs)


old___getattribute__qs = QuerySet.__getattribute__


def __getattribute__qs(self, name):
    if name == '_tt_ts':
        try:
            return old___getattribute__qs(self, '_tt_ts')
        except AttributeError:
            return None

    if get_tt_ts() != self._tt_ts:
        raise TimeTravelQuerySetError(self)

    return old___getattribute__qs(self, name)


old___init__qs = QuerySet.__init__


def __init__qs(self, *args, **kwargs):
    self._tt_ts = get_tt_ts()
    old___init__qs(self, *args, **kwargs)


def patch_safety():
    if not hasattr(Model, '_tt_safety_patched'):
        Model._tt_safety_patched = True
        Model.__getattribute__ = __getattribute__model
        Model.__init__ = __init__model

    if not hasattr(QuerySet, '_tt_safety_patched'):
        QuerySet._tt_safety_patched = True
        QuerySet.__getattribute__ = __getattribute__qs
        QuerySet.__init__ = __init__qs
