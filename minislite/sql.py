# Standard Library
from typing import List, Type

# First Party
from minislite.fields import DatabaseField
from minislite.models import MiniSLiteModel


class SqlManager:
    def __init__(self, model: Type[MiniSLiteModel]):
        self.model = model
        self.data_types = {str: "TEXT", int: "INTEGER", bool: "INTEGER", float: "REAL"}

    def generate_sql_script(self) -> str:
        table_name = self.model.get_table_name()
        field_lines = self.generate_fields_sql_lines()
        fields = ", ".join(field_lines)

        script = f'CREATE TABLE IF NOT EXISTS "{table_name}" ( {fields} );'
        return script

    def generate_fields_sql_lines(self) -> List[str]:
        field_list = self.model.get_fields()
        field_lines = ['"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT']

        for field in field_list:
            field_name = field

            field_obj: DatabaseField = getattr(self.model, field)
            field_type = self.data_types.get(field_obj.field_type, None)
            if field_type is None:
                continue
            not_null = "NOT NULL" if field_obj.not_null else ""
            unique = "UNIQUE" if field_obj.unique else ""
            default = "DEFAULT {0}".format(field_obj.default) if field_obj.default is not None else ""
            auto_increment = "AUTOINCREMENT" if field_obj.auto_increment else ""

            line = f'"{field_name}" {field_type} {not_null} {unique} {default} {auto_increment}'
            field_lines.append(line)

        return field_lines
