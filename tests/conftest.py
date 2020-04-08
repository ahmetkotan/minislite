import pytest


@pytest.fixture()
def mini_model():
    from tests.test_models import MiniModel

    return MiniModel


@pytest.fixture()
def extended_model():
    from tests.test_models import ExtendedModel

    return ExtendedModel


@pytest.fixture()
def database():
    from minislite.minilite import MiniLiteDb

    db = MiniLiteDb("test.db")
    return db
