"""This houses the controller for the repositories. I wanted to have a single context manager for the cursor,
as well as not have to have the repositores do much higher level processing"""

import sqlite3
from contextlib import contextmanager

from personal_budget.table_schema import initialize_db_tables
from personal_budget.repository import AccountRepo
import personal_budget.logger as logger


class RepositoryController:
    def __init__(self, db_connection: sqlite3.Connection, logger_: logger.logging.Logger):
        self._conn = db_connection
        self._logger = logger_

    @contextmanager
    def cursor_manager(self):
        cursor = self._conn.cursor()
        try:
            yield cursor
            self._conn.commit()
        except sqlite3.IntegrityError:
            self._conn.rollback()
            self._logger.exception('sglite3 IntegrityError')
        except Exception:
            self._conn.rollback()
            self._logger.exception('Error occoured')
            raise
        finally:
            cursor.close()