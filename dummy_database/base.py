import threading
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.base.validation import BaseDatabaseValidation
from django.db.backends.utils import CursorWrapper


class InMemoryStorage:
    """In-memory storage for simulating database tables."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern to ensure single storage instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.tables = {}
                    cls._instance.sequences = {}
                    cls._instance._init_system_tables()
        return cls._instance

    def _init_system_tables(self):
        """Initialize Django system tables in memory."""
        # Content types table
        self.tables['django_content_type'] = [
            {'id': 1, 'app_label': 'contenttypes', 'model': 'contenttype'},
            {'id': 2, 'app_label': 'auth', 'model': 'permission'},
            {'id': 3, 'app_label': 'auth', 'model': 'group'},
            {'id': 4, 'app_label': 'auth', 'model': 'user'},
            {'id': 5, 'app_label': 'sessions', 'model': 'session'},
            {'id': 6, 'app_label': 'admin', 'model': 'logentry'},
        ]
        self.sequences['django_content_type_id_seq'] = 100

        # Migrations table
        self.tables['django_migrations'] = []
        self.sequences['django_migrations_id_seq'] = 1

        # Sessions table
        self.tables['django_session'] = []

        # Auth tables
        self.tables['auth_user'] = []
        self.tables['auth_group'] = []
        self.tables['auth_permission'] = []
        self.tables['auth_user_groups'] = []
        self.tables['auth_user_user_permissions'] = []
        self.tables['auth_group_permissions'] = []

        # Admin log table
        self.tables['django_admin_log'] = []

        # Sequences for auto-increment fields
        for table in ['auth_user', 'auth_group', 'auth_permission',
                      'django_admin_log']:
            self.sequences[f'{table}_id_seq'] = 1


class DatabaseFeatures(BaseDatabaseFeatures):
    """Database features declaration - claims all features are supported."""

    allows_group_by_selected_pks = True
    allows_group_by_selected_pks_on_subquery = True
    allows_group_by_selected_pks_with_related = True
    allows_primary_key_0 = True
    allows_unspecified_pk = True
    can_introspect_autofield = True
    can_introspect_big_autofield = True
    can_introspect_binary_field = True
    can_introspect_duration_field = True
    can_introspect_ip_address_field = True
    can_introspect_small_integer_field = True
    can_introspect_time_field = True
    can_introspect_virtual_field = True
    can_return_columns_from_insert = True
    can_return_rows_from_bulk_insert = True
    has_bulk_insert = True
    has_native_uuid_field = True
    has_select_for_update = True
    has_select_for_update_nowait = True
    has_select_for_update_skip_locked = True
    has_real_datatype = True
    supports_aggregate_filter_clause = True
    supports_atomic_references_rename = True
    supports_combined_alters = True
    supports_covering_indexes = True
    supports_expression_indexes = True
    supports_foreign_keys = True
    supports_frame_range_fixed_distance = True
    supports_functions_in_partial_indexes = True
    supports_index_column_ordering = True
    supports_index_on_text_field = True
    supports_ignore_conflicts = True
    supports_inline_foreign_key = True
    supports_json_field = True
    supports_over_clause = True
    supports_parameterized_wrappers = True
    supports_primary_key_on_partition = True
    supports_sequence_reset = True
    supports_subquery_update = True
    supports_table_check_constraints = True
    supports_tablespaces = True
    supports_temporal_subtraction = True
    supports_transactions = True
    supports_update_conflicts = True
    supports_update_conflicts_with_target = True
    supports_unspecified_pk = True
    supports_validate_constraints = True
    supports_window_functions = True
    uses_savepoints = True
    can_connect = True


class DatabaseOperations(BaseDatabaseOperations):
    """Database operations - simulates real database behavior."""

    def quote_name(self, name):
        """Quote a table or column name."""
        return name

    def max_name_length(self):
        """Maximum identifier length."""
        return 63

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        """Clear in-memory tables."""
        storage = InMemoryStorage()
        for table in tables:
            if table in storage.tables:
                if isinstance(storage.tables[table], list):
                    storage.tables[table] = []
        return []

    def last_insert_id(self, cursor, table_name, pk_name):
        """Get the last inserted row ID."""
        return cursor.lastrowid

    def no_limit_value(self):
        """Value used for no limit in queries."""
        return None

    def limit_offset_sql(self, low_mark, high_mark):
        """SQL for LIMIT and OFFSET clauses."""
        return ''

    def date_extract_sql(self, lookup_type, field_name):
        """SQL for date extraction."""
        return field_name

    def date_trunc_sql(self, lookup_type, field_name):
        """SQL for date truncation."""
        return field_name

    def datetime_trunc_sql(self, lookup_type, field_name, tzname):
        """SQL for datetime truncation."""
        return field_name

    def time_trunc_sql(self, lookup_type, field_name):
        """SQL for time truncation."""
        return field_name

    def datetime_cast_date_sql(self, field_name, tzname):
        """SQL for casting datetime to date."""
        return field_name

    def datetime_cast_time_sql(self, field_name, tzname):
        """SQL for casting datetime to time."""
        return field_name

    def datetime_extract_sql(self, lookup_type, field_name, tzname):
        """SQL for extracting parts from datetime."""
        return field_name

    def time_extract_sql(self, lookup_type, field_name):
        """SQL for extracting parts from time."""
        return field_name

    def date_interval_sql(self, timedelta):
        """SQL for date intervals."""
        return ''

    def format_for_duration_arithmetic(self, sql):
        """Format SQL for duration arithmetic."""
        return sql

    def force_no_ordering(self):
        """Force no ordering in queries."""
        return []

    def for_update_sql(self, nowait=False, skip_locked=False, of=()):
        """SQL for SELECT ... FOR UPDATE."""
        return 'FOR UPDATE'

    def pk_default_value(self):
        """Default value for primary key."""
        return 'DEFAULT'

    def random_function_sql(self):
        """SQL for random function."""
        return 'RANDOM()'

    def regex_lookup(self, lookup_type):
        """SQL for regex lookup."""
        return '%s LIKE %s'

    def return_insert_columns(self, fields):
        """SQL for RETURNING clause."""
        return 'RETURNING %s' % ', '.join(f.column for f in fields)

    def savepoint_create_sql(self, sid):
        """SQL for creating a savepoint."""
        return f"SAVEPOINT {sid}"

    def savepoint_rollback_sql(self, sid):
        """SQL for rolling back to a savepoint."""
        return f"ROLLBACK TO SAVEPOINT {sid}"

    def sequence_reset_by_name_sql(self, style, sequences):
        """SQL for resetting sequences."""
        return []

    def sql_for_tablespace(self, tablespace, inline=False):
        """SQL for tablespace clause."""
        return ''

    def validate_autopk_value(self, value):
        """Validate auto-primary key value."""
        return value

    def adapt_datefield_value(self, value):
        """Adapt date field value."""
        return value

    def adapt_datetimefield_value(self, value):
        """Adapt datetime field value."""
        return value

    def adapt_timefield_value(self, value):
        """Adapt time field value."""
        return value

    def adapt_decimalfield_value(self, value, max_digits=None, decimal_places=None):
        """Adapt decimal field value."""
        return value

    def adapt_ipaddressfield_value(self, value):
        """Adapt IP address field value."""
        return value

    def adapt_booleanfield_value(self, value):
        """Adapt boolean field value."""
        return value

    def adapt_floatfield_value(self, value):
        """Adapt float field value."""
        return value

    def adapt_integerfield_value(self, value):
        """Adapt integer field value."""
        return value

    def adapt_small_integerfield_value(self, value):
        """Adapt small integer field value."""
        return value

    def adapt_positive_integerfield_value(self, value):
        """Adapt positive integer field value."""
        return value

    def adapt_positive_small_integerfield_value(self, value):
        """Adapt positive small integer field value."""
        return value


class DatabaseClient(BaseDatabaseClient):
    """Database client - dummy implementation."""

    def runshell(self, parameters):
        """Run database shell."""
        print("Dummy database shell - no actual database")


class DatabaseCreation(BaseDatabaseCreation):
    """Database creation - simulated."""

    def create_test_db(self, verbosity=1, autoclobber=False, serialize=True, keepdb=False):
        """Create a test database."""
        InMemoryStorage()
        return "test_dummy_db"

    def destroy_test_db(self, old_database_name=None, verbosity=1, keepdb=False):
        """Destroy a test database."""
        pass

    def mark_expected_failed_migration(self, migration):
        """Mark an expected failed migration."""
        pass


class DatabaseIntrospection(BaseDatabaseIntrospection):
    """Database introspection - returns information about in-memory tables."""

    def get_table_list(self, cursor):
        """Get list of tables."""
        from django.db.backends.base.introspection import TableInfo
        storage = InMemoryStorage()
        return [TableInfo(name, 't') for name in storage.tables.keys()]

    def get_table_description(self, cursor, table_name):
        """Get table description."""
        return []

    def get_relations(self, cursor, table_name):
        """Get table relations."""
        return {}

    def get_primary_key_column(self, cursor, table_name):
        """Get primary key column name."""
        return 'id'

    def get_sequences(self, cursor, table_name, table_fields=()):
        """Get sequences for a table."""
        storage = InMemoryStorage()
        seq_name = f'{table_name}_id_seq'
        if seq_name in storage.sequences:
            return [{'table': table_name, 'column': 'id'}]
        return []

    def get_key_columns(self, cursor, table_name):
        """Get key columns."""
        return []

    def get_constraints(self, cursor, table_name):
        """Get table constraints."""
        return {}


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    """Schema editor - creates tables in memory."""

    def create_model(self, model):
        """Create a model's table."""
        storage = InMemoryStorage()
        table_name = model._meta.db_table
        if table_name not in storage.tables:
            storage.tables[table_name] = []
            storage.sequences[f'{table_name}_id_seq'] = 1

    def delete_model(self, model):
        """Delete a model's table."""
        storage = InMemoryStorage()
        table_name = model._meta.db_table
        if table_name in storage.tables:
            del storage.tables[table_name]
        seq_name = f'{table_name}_id_seq'
        if seq_name in storage.sequences:
            del storage.sequences[seq_name]

    def add_field(self, model, field):
        """Add a field to a table."""
        pass

    def remove_field(self, model, field):
        """Remove a field from a table."""
        pass

    def alter_field(self, model, old_field, new_field, strict=False):
        """Alter a field."""
        pass


# Exception classes for simulating real database errors
class DatabaseError(Exception):
    """Base database error."""
    pass


class IntegrityError(DatabaseError):
    """Integrity constraint error."""
    pass


class DataError(DatabaseError):
    """Data error."""
    pass


class OperationalError(DatabaseError):
    """Operational database error."""
    pass


class ProgrammingError(DatabaseError):
    """Programming error."""
    pass


class NotSupportedError(DatabaseError):
    """Feature not supported error."""
    pass


class InterfaceError(DatabaseError):
    """Database interface error."""
    pass


class InternalError(DatabaseError):
    """Internal database error."""
    pass


class Database:
    """Class simulating a database module with all exceptions."""

    Error = DatabaseError
    DatabaseError = DatabaseError
    IntegrityError = IntegrityError
    DataError = DataError
    OperationalError = OperationalError
    ProgrammingError = ProgrammingError
    NotSupportedError = NotSupportedError
    InterfaceError = InterfaceError
    InternalError = InternalError


class Cursor:
    """Database cursor with in-memory storage support."""

    def __init__(self):
        self.description = None
        self.rowcount = 0
        self._storage = InMemoryStorage()
        self._last_query = None
        self._last_params = None
        self._results = []
        self._result_index = 0

    def execute(self, sql, params=None):
        """Execute a SQL query."""
        self._last_query = sql
        self._last_params = params
        sql_upper = sql.strip().upper()

        # Simulate various SQL queries
        if sql_upper.startswith('SELECT'):
            self._handle_select(sql, params)
        elif sql_upper.startswith('INSERT'):
            self._handle_insert(sql, params)
        elif sql_upper.startswith('UPDATE'):
            self._handle_update(sql, params)
        elif sql_upper.startswith('DELETE'):
            self._handle_delete(sql, params)
        elif sql_upper.startswith('CREATE TABLE'):
            self._handle_create_table(sql, params)

        return self

    def _handle_select(self, sql, params):
        """Handle SELECT queries."""
        # Simple parser for demonstration
        if 'django_content_type' in sql:
            # Return system content types
            self._results = [
                (1, 'contenttypes', 'contenttype'),
                (2, 'auth', 'permission'),
                (3, 'auth', 'group'),
                (4, 'auth', 'user'),
                (5, 'sessions', 'session'),
                (6, 'admin', 'logentry'),
            ]
            self.description = [('id',), ('app_label',), ('model',)]
            self.rowcount = len(self._results)
        else:
            self._results = []
            self.rowcount = 0

    def _handle_insert(self, sql, params):
        """Handle INSERT queries."""
        table_name = sql.split()[2] if len(sql.split()) > 2 else 'unknown'
        self.rowcount = 1
        # Simulate lastrowid
        seq_name = f'{table_name}_id_seq'
        if seq_name in self._storage.sequences:
            self._storage.sequences[seq_name] += 1
            self._lastrowid = self._storage.sequences[seq_name]
        else:
            self._lastrowid = 1

    def _handle_update(self, sql, params):
        """Handle UPDATE queries."""
        self.rowcount = 1

    def _handle_delete(self, sql, params):
        """Handle DELETE queries."""
        self.rowcount = 0

    def _handle_create_table(self, sql, params):
        """Handle CREATE TABLE queries."""
        table_name = sql.split()[2]
        if table_name not in self._storage.tables:
            self._storage.tables[table_name] = []
            self._storage.sequences[f'{table_name}_id_seq'] = 1

    def executemany(self, sql, param_list):
        """Execute many SQL statements."""
        self.rowcount = len(param_list)
        return self

    def fetchone(self):
        """Fetch one row."""
        if self._result_index < len(self._results):
            result = self._results[self._result_index]
            self._result_index += 1
            return result
        return None

    def fetchall(self):
        """Fetch all rows."""
        return self._results

    def fetchmany(self, size=1):
        """Fetch many rows."""
        results = self._results[self._result_index:self._result_index + size]
        self._result_index += len(results)
        return results

    def close(self):
        """Close the cursor."""
        pass

    def __iter__(self):
        """Iterator over results."""
        return iter(self._results)

    @property
    def lastrowid(self):
        """Get the last inserted row ID."""
        return getattr(self, '_lastrowid', 1)


class DatabaseWrapper(BaseDatabaseWrapper):
    """Main wrapper class for the dummy database backend."""

    vendor = 'dummy'
    display_name = 'Dummy Database'

    # Database as a class attribute
    Database = Database

    features_class = DatabaseFeatures
    ops_class = DatabaseOperations
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    introspection_class = DatabaseIntrospection
    validation_class = BaseDatabaseValidation
    schema_editor_class = DatabaseSchemaEditor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        # Database as an instance attribute
        self.Database = Database
        self._storage = InMemoryStorage()

    def get_connection_params(self):
        """Get connection parameters."""
        return {}

    def get_new_connection(self, conn_params):
        """Get a new connection."""
        return object()  # Return any object to simulate a connection

    def init_connection_state(self):
        """Initialize connection state."""
        pass

    def create_cursor(self, name=None):
        """Create a cursor."""
        return Cursor()

    def _set_autocommit(self, autocommit):
        """Set autocommit mode."""
        pass

    def is_usable(self):
        """Check if the connection is usable."""
        return True

    def cursor(self, name=None):
        """Get a cursor wrapped with CursorWrapper."""
        return CursorWrapper(self.create_cursor(name), self)

    def close(self):
        """Close the connection."""
        pass

    def commit(self):
        """Commit a transaction."""
        pass

    def rollback(self):
        """Rollback a transaction."""
        pass

    def savepoint(self):
        """Create a savepoint."""
        return '1'

    def savepoint_commit(self, sid):
        """Commit a savepoint."""
        pass

    def savepoint_rollback(self, sid):
        """Rollback to a savepoint."""
        pass
