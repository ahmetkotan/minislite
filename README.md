# MiniSLite
MiniSLite is a secure and mini SQLite ORM module.

## Install

### From Pypi

```
pip install minislite
```


### From Source Code

```
git clone https://github.com/ahmetkotan/minislite
cd minislite
python setup.py build
python setup.py install
```

## Usage

### Create Model

```python
from minislite import MiniSLiteModel
from minislite import DatabaseField


class Person(MiniSLiteModel):
    # Only field_type is required
    name = DatabaseField(field_type=str, unique=False, not_null=True, auto_increment=False)
    last_name = DatabaseField(field_type=str, default="mini")
    age = DatabaseField(field_type=int, not_null=False)
    
    # Optionals
    table_name = "person"
    unique_together = ["name", "last_name"]
```
  
### Create Database and Add Model

```python
from minislite import MiniSLiteDb

database = MiniSLiteDb("minis.db")
database.add_model(Person)
```

### Create and Update Object

```python
person1 = Person(name="mini", last_name="slite")
person1.age = 1
person1.save()

person2 = Person.objects.create(name="mini2", last_name="slite")
person2.age = 2
person2.save()
```

### Update All Objects

```python
Person.objects.update(last_name="slite-updated")
```

### Filter/Get and Delete Object

```python
person_objects = Person.objects.filter(last_name="slite-updated")
# or
# person_objects = Person.objects.all()
for person in person_objects:
    print(person.name)

person_obj = Person.objects.get(name="mini")
person_obj.delete()
```

### Delete All Objects

```python
Person.objects.delete(i_am_sure=True)
```

### Clean All Tables or Drop Model

```python
database.clean_tables()
database.drop_model(Person)
```

### Exceptions

```python
from minislite.exceptions import RecordNotFoundError, AlreadyExistsError, DatabaseNotFound, \
    AreYouSure
```

* **RecordNotFoundError:** If you use ``objects.get()`` and that is not found in database
* **AlreadyExistsError:** Raise this exception when an object creating or saving. Check your ``unique=True`` fields and ``unique_together`` fields.
* **DatabaseNotFound:** Cannot use TableManager if you don't initialize ``MiniSLiteDb()``
* **AreYouSure:** Raise this exception if you want to delete all objects(``objects.delete()``) in model. Add ``i_am_sure=True`` arguments.
