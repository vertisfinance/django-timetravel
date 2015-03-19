from django.db.models.options import Options
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.where import ExtraWhere, AND

from . import get_tt_ts, VF, VU


class DBTableDescriptor(object):
    def __get__(self, instance, owner):
        if hasattr(instance, '_tt_model') and get_tt_ts():
            return instance._tt_model._meta.db_table
        else:
            if not hasattr(instance, '_tt_db_table'):
                instance._tt_db_table = instance.__dict__['db_table']

            return instance._tt_db_table

    def __set__(self, instance, value):
        instance._tt_db_table = value


def add_where_if_tt(query, alias):
    tt_ts = get_tt_ts()
    if tt_ts:
        sql = '%s.%s <= %%s AND %s.%s > %%s' % (alias, VF, alias, VU)
        params = (tt_ts, tt_ts)
        query.where.add(ExtraWhere((sql,), params), AND)


def get_from_clause(self):
    result = []
    qn = self
    qn2 = self.connection.ops.quote_name
    first = True
    from_params = []
    for alias in self.query.tables:
        if not self.query.alias_refcount[alias]:
            continue
        try:
            (name, alias, join_type,
             lhs, join_cols, _, join_field) = self.query.alias_map[alias]
        except KeyError:
            # Extra tables can end up in self.tables, but not in the
            # alias_map if they aren't in a join. That's OK. We skip them.
            continue
        alias_str = '' if alias == name else (' %s' % alias)
        add_where_if_tt(self.query, alias)

        if join_type and not first:
            extra_cond = join_field.get_extra_restriction(
                self.query.where_class, alias, lhs)
            if extra_cond:
                extra_sql, extra_params = self.compile(extra_cond)
                extra_sql = 'AND (%s)' % extra_sql
                from_params.extend(extra_params)
            else:
                extra_sql = ""
            result.append('%s %s%s ON (' % (join_type, qn(name), alias_str))
            for index, (lhs_col, rhs_col) in enumerate(join_cols):
                if index != 0:
                    result.append(' AND ')
                params = (qn(lhs), qn2(lhs_col), qn(alias), qn2(rhs_col))
                result.append('%s.%s = %s.%s' % params)
            result.append('%s)' % extra_sql)
        else:
            connector = '' if first else ', '
            result.append('%s%s%s' % (connector, qn(name), alias_str))
        first = False
    for t in self.query.extra_tables:
        alias, unused = self.query.table_alias(t)
        # Only add the alias if it's not already present (the table_alias()
        # calls increments the refcount, so an alias refcount of one means
        # this is the only reference.
        q = self.query
        if alias not in q.alias_map or q.alias_refcount[alias] == 1:
            connector = '' if first else ', '
            result.append('%s%s' % (connector, qn(alias)))
            first = False
            add_where_if_tt(self.query, alias)

    return result, from_params


def patch_fetching():
    if not hasattr(Options, '_tt_fetching_patched'):
        Options._tt_fetching_patched = True
        Options.db_table = DBTableDescriptor()

    if not hasattr(SQLCompiler, '_tt_fetching_patched'):
        SQLCompiler._tt_fetching_patched = True
        SQLCompiler.get_from_clause = get_from_clause
