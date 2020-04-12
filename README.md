# MiniSLite
MiniSLite is a secure and mini SQLite ORM module.

## Install

### From Pypi

The script is [available on PyPI](https://pypi.org/project/minislite/). To install with pip:
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
person1 = Person(name="mini", last_name="slite")  # not created
person1.age = 1
person1.save()  # created

person2 = Person.objects.create(name="mini2", last_name="slite")  # created
person2.age = 2
person2.save()  # updated

person3 = Person.objects.create(name="mini3", last_name="slite", age=10)  # created
person4 = Person.objects.create(name="mini4", last_name="slite", age=20)  # created
```

### Update All Objects

```python
Person.objects.update(last_name="slite-updated")
```

### Filter/Get and Delete Object

```python
first_person = Person.objects.first()
last_person = Person.objects.last()

person_objects = Person.objects.filter(last_name="slite-updated")
# or
# person_objects = Person.objects.all()
for person in person_objects:
    print(person.name)

person_obj = Person.objects.get(name="mini")
person_obj.delete()
```

**Special Filters**
* ``gt``, ``gte``, ``lt``, ``lte`` for integer, bool and float fields
* ``contains``, ``startswith``, ``endswith`` for string fields

```python
older_than_10 = Person.objects.filter(age__gt=10)[0]
print(older_than_10.name)  # mini4
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
from minislite.exceptions import RecordNotFoundError, AlreadyExistsError, DatabaseNotFoundError, \
    AreYouSureError, WhereOperatorError
```

* **RecordNotFoundError:** If you use ``objects.get()`` and that is not found in database
* **AlreadyExistsError:** Raise this exception when an object creating or saving. Check your ``unique=True`` fields and ``unique_together`` fields.
* **DatabaseNotFoundError:** Cannot use TableManager if you don't initialize ``MiniSLiteDb()``
* **AreYouSureError:** Raise this exception if you want to delete all objects(``objects.delete()``) in model. Add ``i_am_sure=True`` arguments.
* **WhereOperatorError:** Raise this exception if you use integer operator for string field. Or vice versa.

## Development and Contribution
See; [CONTRIBUTING.md](CONTRIBUTING.md)
