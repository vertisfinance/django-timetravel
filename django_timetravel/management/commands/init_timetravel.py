from django.core.management.base import NoArgsCommand
from django.apps import apps
from django.db.transaction import atomic

from ... import MIN, create_history_record, insert_history_records


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        chunk_size = options.get('chunk_size', 1000)
        verbosity = options.get('verbosity', 0)
        models = apps.get_models(include_auto_created=True,
                                 include_deferred=True,
                                 include_swapped=True)
        models = [m for m in models if hasattr(m, '_tt_has_history')]
        models = [m for m in models if not m._meta.proxy]
        for i, m in enumerate(models):
            if verbosity:
                msg = u'%s/%s: %s' % (i + 1, len(models), m._meta.model_name)
                self.stdout.write(msg, self.style.MIGRATE_LABEL)

            numobjs = m.objects.all().count()
            with atomic():
                m._tt_model.objects.all().delete()

                collected = []
                for j, obj in enumerate(m.objects.all()):
                    collected.append(create_history_record(m, obj, MIN))
                    if len(collected) == chunk_size:
                        if verbosity:
                            msg = u'    %s/%s' % (j + 1, numobjs)
                            self.stdout.write(msg, ending=' ')
                            self.stdout.write('OK', self.style.MIGRATE_SUCCESS)
                        insert_history_records(m, collected)
                        collected = []

                if collected:
                    if verbosity:
                        msg = u'    %s/%s' % (j + 1, numobjs)
                        self.stdout.write(msg, ending=' ')
                        self.stdout.write('OK', self.style.MIGRATE_SUCCESS)
                    insert_history_records(m, collected)
