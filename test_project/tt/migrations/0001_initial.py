# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tt_auth_group',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, null=True, verbose_name='name')),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
            ],
            options={
                'db_table': 'tt_auth_group',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_auth_group_permissions',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
                ('group', models.BigIntegerField(null=True, db_index=True)),
                ('permission', models.BigIntegerField(null=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_auth_group_permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_auth_permission',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, verbose_name='name')),
                ('codename', models.CharField(max_length=100, null=True, verbose_name='codename')),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
                ('content_type', models.BigIntegerField(null=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_auth_permission',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_auth_user',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, null=True, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, null=True, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='date joined')),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
            ],
            options={
                'db_table': 'tt_auth_user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_auth_user_groups',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
                ('user', models.BigIntegerField(null=True, db_index=True)),
                ('group', models.BigIntegerField(null=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_auth_user_groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_auth_user_user_permissions',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
                ('user', models.BigIntegerField(null=True, db_index=True)),
                ('permission', models.BigIntegerField(null=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_auth_user_user_permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_derivative_futures',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
                ('underlying', models.BigIntegerField(null=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_derivative_futures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_django_admin_log',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField(auto_now=True, verbose_name='action time', null=True)),
                ('object_id', models.TextField(null=True, verbose_name='object id', blank=True)),
                ('object_repr', models.CharField(max_length=200, null=True, verbose_name='object repr')),
                ('action_flag', models.PositiveSmallIntegerField(null=True, verbose_name='action flag')),
                ('change_message', models.TextField(null=True, verbose_name='change message', blank=True)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
                ('user', models.BigIntegerField(null=True, db_index=True)),
                ('content_type', models.BigIntegerField(null=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_django_admin_log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_django_content_type',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('app_label', models.CharField(max_length=100, null=True)),
                ('model', models.CharField(max_length=100, null=True, verbose_name='python model class name')),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
            ],
            options={
                'db_table': 'tt_django_content_type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_django_session',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('tt_orig_id', models.CharField(max_length=40, verbose_name='session key', db_index=True)),
                ('session_data', models.TextField(null=True, verbose_name='session data')),
                ('expire_date', models.DateTimeField(null=True, verbose_name='expire date', db_index=True)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_django_session',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_product_product',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
            ],
            options={
                'db_table': 'tt_product_product',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tt_product_product_maintainers',
            fields=[
                ('tt_valid_until_ts', models.DecimalField(default=999999999999, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_valid_from_ts', models.DecimalField(default=0, auto_created=True, max_digits=18, decimal_places=6)),
                ('tt_id', models.AutoField(verbose_name=b'tt_id', serialize=False, auto_created=True, primary_key=True)),
                ('tt_create_modif_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_delete_user_id', models.BigIntegerField(serialize=False, null=True, auto_created=True, db_index=True)),
                ('tt_orig_id', models.BigIntegerField(db_index=True)),
                ('product', models.BigIntegerField(null=True, db_index=True)),
                ('user', models.BigIntegerField(null=True, db_index=True)),
            ],
            options={
                'db_table': 'tt_product_product_maintainers',
            },
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name='tt_product_product_maintainers',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_product_product',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_django_session',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_django_content_type',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_django_admin_log',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_derivative_futures',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_auth_user_user_permissions',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_auth_user_groups',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_auth_user',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_auth_permission',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_auth_group_permissions',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
        migrations.AlterIndexTogether(
            name='tt_auth_group',
            index_together=set([('tt_orig_id', 'tt_valid_until_ts')]),
        ),
    ]
