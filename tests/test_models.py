# First Party
import pytest
from minislite.fields import DatabaseField
from minislite.models import MiniSLiteModel
from minislite.minislite import MiniSLiteDb
from minislite.exceptions import AlreadyExistsError


class MiniModel(MiniSLiteModel):
    name = DatabaseField(field_type=str)
    unknown = DatabaseField(field_type=dict)


class ExtendedModel(MiniSLiteModel):
    name = DatabaseField(field_type=str)
    last_name = DatabaseField(field_type=str, default="last_name")
    age = DatabaseField(field_type=int, not_null=False)

    table_name = "extended_model"
    unique_together = ["name", "last_name"]


def test_models_initialize(database: MiniSLiteDb):
    database.add_model(ExtendedModel)
    database.clean_tables()

    extended = ExtendedModel(name="extended")
    assert extended.name == "extended"
    assert extended.last_name == "last_name"
    assert extended.age is None
    assert extended.manager


def test_models_reload_attributes(database: MiniSLiteDb):
    database.add_model(ExtendedModel)
    database.clean_tables()

    extended = ExtendedModel(name="extended")
    extended.reload_attributes(last_name="model1")

    assert extended.name == "extended"
    assert extended.last_name == "model1"
    assert extended.id is None

    extended.reload_attributes(id=1)
    assert extended.id == 1


def test_models_save(database: MiniSLiteDb):
    database.add_model(ExtendedModel)
    database.clean_tables()

    extended = ExtendedModel(name="extended")
    extended.last_name = "test_models_save"
    extended.age = 1

    assert extended.id is None
    extended.save()
    assert extended.id is not None

    check_created = ExtendedModel.objects.get(last_name="test_models_save")
    assert check_created.age == 1

    extended.age = 3
    extended.save()

    check_updated = ExtendedModel.objects.get(age=3)

    assert len(ExtendedModel.objects.all()) == 1
    assert check_updated.age == 3


def test_models_save_2(database: MiniSLiteDb):
    database.add_model(ExtendedModel)
    database.clean_tables()

    ExtendedModel.objects.create(name="extented", last_name="model", age=1)
    extended = ExtendedModel.objects.create(name="extented", last_name="model2", age=1)
    extended.last_name = "model"

    with pytest.raises(AlreadyExistsError):
        extended.save()

    extended.delete()
    assert ExtendedModel.objects.filter(id=extended.id) == []


def test_models_class_methods():
    extended = ExtendedModel()
    mini = MiniModel()

    assert extended.get_table_name() == "extended_model"
    assert mini.get_table_name() == "minimodel"

    assert extended.get_unique_together() == ["name", "last_name"]
    assert mini.get_unique_together() == []

    assert extended.get_fields() == ["name", "last_name", "age"]
    assert mini.get_fields() == ["name", "unknown"]
