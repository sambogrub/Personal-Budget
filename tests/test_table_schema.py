"""This is to test the creation of the tables needed"""

import sqlite3
import pytest
from unittest.mock import MagicMock

from personal_budget.table_schema import initialize_db_tables

@pytest.fixture
def setup_db_and_logger():
    conn = sqlite3.connect(":memory:")
    mock_logger = MagicMock()
    yield conn, mock_logger
    conn.close()

def test_initialize_db_tables_success(setup_db_and_logger):
    conn, mock_logger = setup_db_and_logger

    initialize_db_tables(conn, mock_logger)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = {row[0] for row in cursor.fetchall()}

    expected_tables = {'accounts', 'categories', 'budget', 'transactions'}
    assert tables == expected_tables, "Not all expected tables were created"

def test_logger_called_on_integrity_error(setup_db_and_logger):
    """Test that the logger is called when an integrity error occurs."""
    conn, mock_logger = setup_db_and_logger

    initialize_db_tables(conn, mock_logger)

    with pytest.raises(sqlite3.OperationalError):
        initialize_db_tables(conn, mock_logger)

    mock_logger.exception.assert_called()

