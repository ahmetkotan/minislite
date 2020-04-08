# Standard Library
import os
import sqlite3

# First Party
from minislite.exceptions import DatabaseNotFound


class TableManager:
    def __init__(self, table_name) -> None:
        db_file = os.environ.get("MINILITE_DB_PATH", None)
        if db_file is None:
            raise DatabaseNotFound("Database not defined.")

        self.table_name = table_name
        self.connection = sqlite3.connect(db_file)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

    def select(self, **kwargs) -> sqlite3.Cursor:
        if kwargs.values():
            column_list = []
            values = []
            for key, value in kwargs.items():
                if value is None:
                    where = f"{key} IS NULL"
                else:
                    values.append(value)
                    where = f"{key} = ?"
                column_list.append(where)

            columns = " AND ".join(column_list)
            tuple_values = tuple(values)

            query = f"SELECT * FROM {self.table_name} WHERE {columns}"
        else:
            tuple_values = ()
            query = f"SELECT * FROM {self.table_name}"

        return self.cursor.execute(query, tuple_values)

    def insert(self, **kwargs) -> int:
        columns = ",".join(kwargs.keys())
        values = ",".join(["?" for _ in kwargs.keys()])

        query = f"INSERT INTO {self.table_name} ({columns}) "
        query += f"VALUES ({values})"
        tuple_values = tuple(kwargs.values())

        self.cursor.execute(query, tuple_values)
        self.connection.commit()
        return self.cursor.lastrowid

    def update(self, object_id=None, **kwargs) -> None:
        if not kwargs.values():
            return
        column_list = []
        for key in kwargs.keys():
            set_column = f"{key} = ?"
            column_list.append(set_column)

        columns = ", ".join(column_list)
        values = list(kwargs.values())

        query = f"UPDATE {self.table_name} SET {columns}"
        if object_id:
            query += f" WHERE id = ?"
            values.append(object_id)

        tuple_values = tuple(values)
        self.cursor.execute(query, tuple_values)
        self.connection.commit()

    def delete(self, object_id=None) -> None:
        query = f"DELETE FROM {self.table_name}"
        if object_id:
            query += " WHERE id = ?"
            tuple_values = (object_id,)
            self.cursor.execute(query, tuple_values)
        else:
            self.cursor.execute(query)

        self.connection.commit()
