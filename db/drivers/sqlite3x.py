import sqlite3

import db
from db.drivers import Driver

from collections import namedtuple


def _namedtuple_factory(cursor, row):
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def connect(*args, **kwargs):
    """Wraps sqlite3.connect forcing the options required for a
       db style connection to work.  As of this writing that consists
       of installing a NamedTupleCursor factory but may grow more involved
       over time as things change.
    """

    conn = sqlite3.connect(*args, **kwargs)
    conn.row_factory = _namedtuple_factory
    return conn


class Sqlite3Driver(Driver):

    PARAM_STYLE = "qmark"

    def __init__(self, conn_string, **kwargs):
        super(Sqlite3Driver, self).__init__(conn_string)
        self.conn = connect(self.conn_string, **kwargs)

    def connect(self):
        return self.conn


register = Sqlite3Driver.register
