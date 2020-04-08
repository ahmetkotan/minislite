from minislite.minilite import MiniLiteDb
from tests.test_models import MiniModel


def test_minilite_initialize():
    db = MiniLiteDb()
    assert db.cursor


def test_minilite_add_model(mini_model: MiniModel):
    db = MiniLiteDb()
    db.add_model(mini_model)

    test_models = db.cursor.execute('SELECT * FROM minimodel').fetchall()
    assert test_models == []


def test_minilite_drop_model(mini_model: MiniModel, database: MiniLiteDb):
    database.add_model(mini_model)
    database.drop_model(mini_model)

    table_list = database.cursor.execute("SELECT * FROM sqlite_sequence WHERE name = 'minimodel'").fetchall()
    assert len(table_list) == 0


def test_minilite_clean_tables(mini_model: MiniModel, database: MiniLiteDb):
    database.add_model(mini_model)

    database.cursor.execute("INSERT INTO minimodel (name) VALUES ('mini')")
    database.connection.commit()

    mini = dict(database.cursor.execute("SELECT * FROM minimodel").fetchone())
    assert mini.get('name') == "mini"

    database.clean_tables()
    cleaned_mini = database.cursor.execute("SELECT * FROM minimodel").fetchone()
    assert cleaned_mini is None
