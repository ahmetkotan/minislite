# Standard Library
import os

# First Party
import pytest
from minislite.models import MiniSLiteModel
from minislite.tables import TableManager
from minislite.minislite import MiniSLiteDb
from minislite.exceptions import DatabaseNotFoundError, RecordNotFoundError, WhereOperatorError


def test_tables_initialize(extended_model: MiniSLiteModel):
    os.environ.pop("MINISLITE_DB_PATH", None)

    with pytest.raises(DatabaseNotFoundError):
        TableManager(model=extended_model)

    database = MiniSLiteDb("test.db")
    database.add_model(extended_model)

    TableManager(extended_model)
    assert database.connection
    assert database.cursor


def test_tables_get_special_key_values(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)

    table = TableManager(extended_model)
    key, operator, value = table.get_special_key_values("name__contains", "extended")

    assert key == "name"
    assert operator == "LIKE"
    assert value == "%extended%"

    with pytest.raises(WhereOperatorError):
        table.get_special_key_values("name__gt", "extended")


def test_tables_select(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    table = TableManager(extended_model)

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


def test_tables_select_with_operators(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    extended_model.objects.create(name="extended", last_name="operator1", age=10)
    extended_model.objects.create(name="extended", last_name="operator2", age=20)
    extended_model.objects.create(name="extended", last_name="operator3", age=30)
    extended_model.objects.create(name="extended2", last_name="notoperator4", age=None)

    table = TableManager(extended_model)
    assert len(table.select(last_name__contains="operator").fetchall()) == 4
    assert len(table.select(last_name__startswith="operator").fetchall()) == 3
    assert len(table.select(last_name__endswith="4").fetchall()) == 1

    assert len(table.select(age__gt=20).fetchall()) == 1
    assert len(table.select(age__gte=20).fetchall()) == 2


def test_tables_insert(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    table = TableManager(extended_model)
    table.insert(name="extended", last_name="model1", age=1)

    assert len(extended_model.objects.all()) == 1


def test_tables_update(extended_model: MiniSLiteModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    table = TableManager(extended_model)
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

    table = TableManager(extended_model)

    extended = extended_model.objects.create(name="extended", last_name="model2", age=2)
    extended_model.objects.create(name="extended", last_name="model3", age=3)
    extended_model.objects.create(name="extended2", last_name="model4", age=None)

    table.delete(object_id=extended.id)

    with pytest.raises(RecordNotFoundError):
        extended_model.objects.get(id=extended.id)
    assert len(extended_model.objects.all()) == 2

    table.delete()
    assert len(extended_model.objects.all()) == 0
