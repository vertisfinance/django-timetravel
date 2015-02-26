import copy

from django.db.models import signals, Model, ForeignKey, OneToOneField
from django.db.models import ManyToManyField
from django.db.models.fields.related import ManyToOneRel
from django.utils import six
from django.conf import settings


class TimeTravel(object):
    """
    Add this class as a mixin to your model bases to trigger timetravel
    functionality.
    It is also OK to register the model with `timetravelify(<model>)`.
    """
    @property
    def _timetravel_needed(self):
        return True


processed_models = set()
timetraveled_models = set()


def get_migration_app():
    """
    If you use timetravel this key must be set in settings.
    The app specified here must be present in INSTALLED_APPS.
    """
    if hasattr(settings, 'TIMETRAVEL_MIGRATION_APP'):
        return settings.TIMETRAVEL_MIGRATION_APP
    raise Exception('No migration app given')


def related_models(model):
    """
    Get all processed models pointed by
    (ManyToOneRel or OneToOneRel) `model`.
    """
    ret = set()
    for field in model._meta.fields:
        rel = field.rel
        if rel and all([isinstance(rel, ManyToOneRel),  # contains OneToOneRel
                        not isinstance(rel, six.string_types),
                        rel.to in processed_models]):
            ret.add(rel.to)
    return ret


def all_tt_related_models():
    """
    Returns all processed related models in timetraveled_models.
    """
    return reduce(lambda s1, s2: s1.union(related_models(s2)),
                  timetraveled_models,
                  set())


def all_related_to_tt_models():
    """
    Returns all processed models pointed to by any timetraveled model.
    """
    return [m for m in processed_models
            if related_models(m).intersection(timetraveled_models)]


def process_model(sender, **kwargs):
    """
    Listens to class_prepared signal.
    """
    if any([hasattr(sender, '_timetravel_model'),
            sender.__module__ == '__fake__']):
        return

    if getattr(sender, '_timetravel_needed', None):
        timetravelify(sender)

    # processed models those point to any timetraveled model
    points_to_tt = all_related_to_tt_models()
    for _model in points_to_tt:
        timetravelify(_model)

    # processed models pointed by any timetraveled modes
    for _model in all_tt_related_models():
        timetravelify(_model)

    processed_models.add(sender)


def timetravelify(model):
    """
    Makes the given model timetravel capable.
    """
    if any([hasattr(model, '_timetravel_model'),
            model.__module__ == '__fake__',
            model in timetraveled_models]):
        return

    create_timetravel_model(for_model=model)
    timetraveled_models.add(model)


def create_timetravel_model(for_model):
    """
    Returns the newly created timetravel model class for the
    model given.
    """
    migration_module = '%s.models' % get_migration_app()
    attrs = {'__module__': migration_module}

    fields = copy_fields(for_model)
    attrs.update(fields)
    attrs.update({'_timetravel_model': True})
    name = '%s_%s' % (for_model._meta.app_label, for_model._meta.model_name)
    return type(str(name), (Model,), attrs)


def copy_fields(model):
    """
    Creates copies of the model's original fields, returning
    a dictionary mapping field name to copied field object.
    """
    fields = {}

    # print model._meta.model_name
    # for f in model._meta.fields:
    #     print '    %s' % f
    # print '--- locals ---'
    # for f in model._meta.local_fields:
    #     print '    %s' % f

    for field in model._meta.local_fields:
        if isinstance(field, ForeignKey):
            to_model_meta = field.rel.to._meta
            migration_app = get_migration_app()
            app_label = to_model_meta.app_label
            model_name = to_model_meta.model_name
            rel_name = field.related.get_accessor_name()
            _field = ForeignKey('%s.%s_%s' % (migration_app,
                                              app_label,
                                              model_name),
                                related_name=rel_name)
            _field.name = field.name
        elif isinstance(field, OneToOneField):
            continue
        elif isinstance(field, ManyToManyField):
            continue
        else:
            _field = copy.copy(field)

        # field.rel = copy.copy(field.rel)
        # if isinstance(field, models.ForeignKey):
        #     # Don't allow reverse relations.
        #     # ForeignKey knows best what datatype to use for the column
        #     # we'll used that as soon as it's finalized by copying rel.to
        #     field.__class__ = CustomForeignKeyField
        #     field.rel.related_name = '+'
        #     field.null = True
        #     field.blank = True
        # if isinstance(field, OrderWrt):
        #     # OrderWrt is a proxy field, switch to a plain IntegerField
        #     field.__class__ = models.IntegerField
        # transform_field(field)

        fields[_field.name] = _field
    return fields


signals.class_prepared.connect(process_model,
                               dispatch_uid='any')
