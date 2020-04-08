# First Party
from minislite.sql import SqlManager


def test_sql_generate_fields(mini_model):
    sql_manager = SqlManager(mini_model)

    field_lines = sql_manager.generate_fields_sql_lines()

    id_line = field_lines[0]
    name_line = field_lines[1]

    assert len(field_lines) == 2
    assert id_line == '"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT'
    assert name_line.startswith('"name" TEXT NOT NULL')


def test_sql_generate(mini_model):
    sql_manager = SqlManager(mini_model)

    sql_script = sql_manager.generate_sql_script()

    assert sql_script.startswith('CREATE TABLE IF NOT EXISTS "minimodel"')
