# First Party
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
    from minislite.minislite import MiniSLiteDb

    db = MiniSLiteDb("test.db")
    return db
