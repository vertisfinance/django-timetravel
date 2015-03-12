import copy

from django.apps.config import AppConfig
from django.apps import apps
from django.conf import settings
from django.db.models import signals, Model, ForeignKey, OneToOneField
from django.db.models.fields import (AutoField, BigIntegerField, DecimalField,
                                     BooleanField)
from .queryset import patch_queryset
from . import FORBIDDEN_FIELDS, MAX, PK, OK, CU, DU, VF, VU


seen_models = set()
installed_app_labels = [AppConfig.create(entry).label
                        for entry in settings.INSTALLED_APPS]


def get_migration_app():
    """
    If you use timetravel this key must be set in settings.
    The app specified here must be present in INSTALLED_APPS.
    """
    if hasattr(settings, 'TIMETRAVEL_MIGRATION_APP'):
        return settings.TIMETRAVEL_MIGRATION_APP
    raise Exception('No migration app given')


def process_models(sender, **kwargs):
    do_patch()

    all_models = apps.all_models
    for app_label in all_models:
        if app_label not in installed_app_labels:
            continue
        app_models = all_models[app_label]
        for model_name in app_models:
            entry = '%s.%s' % (app_label, model_name)
            model = app_models[model_name]

            if entry not in seen_models and all_relations_ready(model):
                seen_models.add(entry)
                create_timetravel_model(model)

    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    entry = '%s.%s' % (app_label, model_name)

    if app_label in installed_app_labels:
        if entry not in seen_models and all_relations_ready(sender):
            seen_models.add(entry)
            create_timetravel_model(sender)


def all_relations_ready(model):
    for field in model._meta.local_fields:
        if field.rel:
            if not hasattr(field.rel.to, '_meta'):
                return False
            if not field.rel.to._meta.pk:
                return False
    try:
        get_user_model()
    except LookupError:
        return False
    return True


def create_timetravel_model(for_model):
    """
    Returns the newly created timetravel model class for the
    model given.
    """
    if any([hasattr(for_model, '_tt_is_timetravel_model'),
            for_model.__module__ == '__fake__']):
        return

    opt = for_model._meta
    name = 'tt_%s' % opt.db_table

    class Meta:
        app_label = get_migration_app()
        db_table = name
        index_together = [[OK, VU]]

    attrs = {'Meta': Meta,
             '_tt_is_timetravel_model': True,
             '__module__': for_model.__module__}

    fields = copy_fields(for_model)
    attrs.update(fields)

    for_model._tt_has_history = True
    ret = type(str(name), (Model,), attrs)
    for_model._tt_model = ret
    return ret


def auto_to_integer(field):
    _field = BigIntegerField()
    _field.name = field.name
    _field.db_index = field.db_index
    _field.verbose_name = field.verbose_name
    _field.db_column = field.db_column
    _field.db_tablespace = field.db_tablespace
    _field.primary_key = field.primary_key
    _field.serialize = field.serialize
    _field.null = field.null
    _field._unique = field._unique
    _field.unique_for_date = field.unique_for_date
    _field.unique_for_month = field.unique_for_month
    _field.unique_for_year = field.unique_for_year

    return _field


def get_user_model():
    aum = settings.AUTH_USER_MODEL
    app_label, model_name = aum.split('.')
    return apps.get_registered_model(app_label, model_name)


def create_user_field(name):
    user_field = get_user_model()._meta.pk

    if isinstance(user_field, AutoField):
        user_field = auto_to_integer(user_field)
    else:
        user_field = copy.copy(user_field)

    user_field.name = name
    user_field.primary_key = False
    user_field.null = True
    user_field.db_index = True
    user_field.auto_created = True

    return user_field


def copy_fields(model):
    """
    Creates copies of the model's original fields, returning
    a dictionary mapping field name to copied field object.
    """
    fields = {
        PK: AutoField(verbose_name=PK,
                      primary_key=True,
                      auto_created=True),
        CU: create_user_field(CU),
        DU: create_user_field(DU),
        VF: DecimalField(max_digits=18, decimal_places=6, default=0,
                         auto_created=True),
        VU: DecimalField(max_digits=18, decimal_places=6, default=MAX,
                         auto_created=True)}

    for field in model._meta.local_fields:
        if field.name in FORBIDDEN_FIELDS.values():
            raise Exception('Can not use `%s` as a field name '
                            'with django-timetravel')

        if isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
            _field = copy.copy(field.rel.to._meta.pk)
            _field.name = field.name
            _field.primary_key = False
            _field.db_index = True
        else:
            _field = copy.copy(field)

        if isinstance(_field, AutoField):
            _field = auto_to_integer(field)

        _field._tt_field_attrname = field.attname
        _field._tt_field_name = field.name

        if not isinstance(_field, BooleanField):
            _field.null = True

        if _field.primary_key:
            _field.primary_key = False
            _field.serialize = True
            _field.name = OK
            _field.db_index = True
            _field.null = False

        _field._unique = False
        _field.unique_for_date = False if _field.unique_for_date else None
        _field.unique_for_month = False if _field.unique_for_month else None
        _field.unique_for_year = False if _field.unique_for_year else None

        _field.auto_created = False

        fields[_field.name] = _field

    # print model._meta.model_name
    # for fn, f in fields.items():
    #     print '    %s: %s' % (fn, f.__class__)

    return fields


def do_patch():
    patch_queryset()


signals.class_prepared.connect(process_models, dispatch_uid='any')
