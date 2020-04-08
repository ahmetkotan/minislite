# Standard Library
import os

# First Party
import pytest
from minislite.models import MiniSLiteModel
from minislite.tables import TableManager
from minislite.minislite import MiniSLiteDb
from minislite.exceptions import DatabaseNotFound, RecordNotFoundError


def test_tables_initialize(extended_model: MiniSLiteModel):
    os.environ.pop("MINILITE_DB_PATH")

    with pytest.raises(DatabaseNotFound):
        TableManager(table_name="x")

    database = MiniSLiteDb("test.db")
    database.add_model(extended_model)

    TableManager(extended_model.get_table_name())
    assert database.connection
    assert database.cursor


def test_tables_select(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    table = TableManager(extended_model.get_table_name())

    extended = extended_model.objects.create(name="extended", last_name="model1", age=None)
    extended_model.objects.create(name="extended", last_name="model2", age=2)
    extended_model.objects.create(name="extended", last_name="model3", age=3)
    extended_model.objects.create(name="extended2", last_name="model4", age=None)

    all_select = table.select()
    assert len(all_select.fetchall()) == 4

    select_with_null = table.select(name="extended", age=None).fetchone()
    assert dict(select_with_null).get("id") == extended.id

    select = table.select(name="extended").fetchall()
    assert len(select) == 3

    first_extended = table.select(name="extended", order_by="id", limit=1).fetchone()
    assert dict(first_extended).get("last_name") == "model1"

    last_extended = table.select(name="extended", order_by="-id", limit=1).fetchone()
    assert dict(last_extended).get("last_name") == "model3"


def test_tables_insert(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    table = TableManager(extended_model.get_table_name())
    table.insert(name="extended", last_name="model1", age=1)

    assert len(extended_model.objects.all()) == 1


def test_tables_update(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    table = TableManager(extended_model.get_table_name())
    assert table.update() is None

    extended = extended_model.objects.create(name="extended", last_name="model2", age=2)
    extended_model.objects.create(name="extended", last_name="model3", age=3)

    table.update(name="extended1")
    all_extended = extended_model.objects.all()

    for i in all_extended:
        assert i.name == "extended1"

    table.update(object_id=extended.id, name="extended2")
    assert extended_model.objects.get(id=extended.id).name == "extended2"


def test_tables_delete(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    table = TableManager(extended_model.get_table_name())

    extended = extended_model.objects.create(name="extended", last_name="model2", age=2)
    extended_model.objects.create(name="extended", last_name="model3", age=3)
    extended_model.objects.create(name="extended2", last_name="model4", age=None)

    table.delete(object_id=extended.id)

    with pytest.raises(RecordNotFoundError):
        extended_model.objects.get(id=extended.id)
    assert len(extended_model.objects.all()) == 2

    table.delete()
    assert len(extended_model.objects.all()) == 0
