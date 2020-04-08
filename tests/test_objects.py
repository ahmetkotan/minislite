# First Party
import pytest
from tests.test_models import MiniModel, ExtendedModel
from minislite.minislite import MiniSLiteDb
from minislite.exceptions import AreYouSure, AlreadyExistsError, RecordNotFoundError


def test_objects_dunder_get(extended_model: ExtendedModel):
    assert extended_model.objects.table_name == "extended_model"
    assert extended_model.objects.klass == extended_model
    assert extended_model.objects.unique_together == ["name", "last_name"]
    assert extended_model.objects.manager


def test_objects_get(extended_model: ExtendedModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    with pytest.raises(RecordNotFoundError):
        extended_model.objects.get(name="extended")

    extended_model.objects.create(name="extended", last_name="model", age=1)
    extended_obj = extended_model.objects.get(name="extended")

    assert isinstance(extended_obj, extended_model)
    assert extended_obj.last_name == "model"


def test_objects_filter(extended_model: ExtendedModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    extended_model.objects.create(name="extended", last_name="model", age=1)
    extended_model.objects.create(name="extended", last_name="model2", age=1)
    extended_model.objects.create(name="extended", last_name="model3", age=2)

    filtered_extended = extended_model.objects.filter(age=1)
    assert len(filtered_extended) == 2
    assert filtered_extended[0].name == "extended"

    empty_extended = extended_model.objects.filter(last_name="model4")
    assert len(empty_extended) == 0


def test_objects_all(extended_model: ExtendedModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    extended_model.objects.create(name="extended", last_name="model", age=1)
    extended_model.objects.create(name="extended", last_name="model2", age=1)
    extended_model.objects.create(name="extended", last_name="model3", age=1)
    all_extended = extended_model.objects.all()

    assert len(all_extended) == 3


def test_objects_first_last(extended_model: ExtendedModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    extended_model.objects.create(name="extended", last_name="model", age=1)
    extended_model.objects.create(name="extended", last_name="model2", age=1)
    extended_model.objects.create(name="extended", last_name="model3", age=1)

    first_object = extended_model.objects.first()
    assert first_object.last_name == "model"

    last_object = extended_model.objects.last()
    assert last_object.last_name == "model3"


def test_objects_check_unique_together(extended_model: ExtendedModel, mini_model: MiniModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.add_model(mini_model)
    database.clean_tables()

    mini_model.objects.create(name="mini")
    assert mini_model.objects.check_unique_together(name="mini") is True

    extended = extended_model.objects.create(name="extended", last_name="model", age=1)
    is_creating_check = extended_model.objects.check_unique_together(
        is_creating=True, name="extended", last_name="model"
    )
    assert is_creating_check is False
    is_creating_check_false = extended_model.objects.check_unique_together(
        is_creating=True, name="extended", last_name="model2"
    )
    assert is_creating_check_false is True

    update_check = extended_model.objects.check_unique_together(name="extended", last_name="model")
    assert update_check is False

    extended = extended_model.objects.get(name="extended", last_name="model")
    update_check_with_object = extended_model.objects.check_unique_together(
        name="extended", last_name="model", object_id=extended.id
    )
    assert update_check_with_object is True


def test_objects_update(extended_model: ExtendedModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    extended1 = extended_model.objects.create(name="extended", last_name="model", age=1)
    extended_model.objects.create(name="extended", last_name="model2", age=2)
    extended_model.objects.create(name="extended", last_name="model3", age=1)

    with pytest.raises(AlreadyExistsError):
        extended_model.objects.update(name="extended", last_name="model3")

    extended_model.objects.update(object_id=extended1.id, name="extended", age=3)
    updated_extended1 = extended_model.objects.get(id=extended1.id)
    assert updated_extended1.age == 3


def test_objects_create(extended_model: ExtendedModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    model = extended_model.objects.create(name="extended", last_name="model", age=1)

    assert model.name == "extended"
    assert model.last_name == "model"
    assert model.age == 1

    with pytest.raises(AlreadyExistsError):
        extended_model.objects.create(name="extended", last_name="model", age=2)


def test_objects_delete(extended_model: ExtendedModel, database: MiniSLiteDb):
    database.add_model(extended_model)
    database.clean_tables()

    extended1 = extended_model.objects.create(name="extended", last_name="model", age=1)
    extended_model.objects.create(name="extended", last_name="model2", age=2)
    extended_model.objects.create(name="extended", last_name="model3", age=3)

    with pytest.raises(AreYouSure):
        extended_model.objects.delete()

    extended_model.objects.delete(object_id=extended1.id)
    assert len(extended_model.objects.all()) == 2

    extended_model.objects.delete(i_am_sure=True)
    assert len(extended_model.objects.all()) == 0
