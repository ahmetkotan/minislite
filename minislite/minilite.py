# Standard Library
import os
import sqlite3
from typing import Type

# First Party
from minislite.sql import SqlManager
from minislite.models import MiniLiteModel


class MiniLiteDb:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        os.environ["MINILITE_DB_PATH"] = self.db_path

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

    def add_model(self, model: Type[MiniLiteModel]):
        sql_manager = SqlManager(model)
        sql_script = sql_manager.generate_sql_script()

        self.cursor.executescript(sql_script)
        self.connection.commit()

    def drop_model(self, model: Type[MiniLiteModel]):
        table_name = model.get_table_name()
        self.cursor.execute(f"DROP TABLE {table_name}")
        self.connection.commit()

    def clean_tables(self):
        table_list = self.cursor.execute("SELECT name FROM sqlite_sequence").fetchall()
        for table in table_list:
            table_name = dict(table).get('name')
            self.cursor.execute(f"DELETE FROM {table_name}")

        self.connection.commit()
