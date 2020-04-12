# Standard Library
import os
import sqlite3
from typing import Any, Dict, Tuple, Optional

# First Party
from minislite.exceptions import WhereOperatorError, DatabaseNotFoundError


class TableManager:
    def __init__(self, model) -> None:
        db_file = os.environ.get("MINISLITE_DB_PATH", None)
        if db_file is None:
            raise DatabaseNotFoundError("Database not defined.")

        self.model = model
        self.table_name = model.get_table_name()
        self.connection = sqlite3.connect(db_file)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.integer_operators = {
            "gt": {"operator": ">", "value_format": "{0}"},
            "gte": {"operator": ">=", "value_format": "{0}"},
            "lt": {"operator": "<=", "value_format": "{0}"},
            "lte": {"operator": "<=", "value_format": "{0}"},
        }
        self.string_operators = {
            "contains": {"operator": "LIKE", "value_format": "%{0}%"},
            "startswith": {"operator": "LIKE", "value_format": "{0}%"},
            "endswith": {"operator": "LIKE", "value_format": "%{0}"},
        }

        self.operators = {
            int: self.integer_operators,
            bool: self.integer_operators,
            float: self.integer_operators,
            str: self.string_operators,
        }

    def get_special_key_values(self, key, value) -> Tuple[Any, Optional[str], Any]:
        if value is None:
            return key, "IS", None

        if "__" in key:
            operator_key = key.split("__")[1]
            key = key.split("__")[0]
            field_type = getattr(self.model, key).field_type

            operator_list: Optional[Dict[str, Dict[str, str]]]
            operator_list = self.operators.get(field_type)
            parameters = operator_list.get(operator_key, None)  # type: ignore
            if parameters is None:
                raise WhereOperatorError(f"{operator_key} operator not found for {key}")

            operator = parameters.get("operator")
            value_format = parameters.get("value_format")
            value = value_format.format(value)  # type: ignore
            return key, operator, value

        return key, "=", value

    def select(self, order_by: str = "", limit: int = 0, **kwargs) -> sqlite3.Cursor:
        if kwargs.values():
            column_list = []
            values = []
            for key, value in kwargs.items():
                key, operator, value = self.get_special_key_values(key, value)
                where = f"{key} {operator} ?"
                values.append(value)

                column_list.append(where)

            columns = " AND ".join(column_list)
            tuple_values = tuple(values)

            query = f"SELECT * FROM {self.table_name} WHERE {columns}"
        else:
            tuple_values = ()
            query = f"SELECT * FROM {self.table_name}"

        if order_by:
            query += f" ORDER BY {order_by} ASC"

        if limit:
            query += f" LIMIT {limit}"

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
