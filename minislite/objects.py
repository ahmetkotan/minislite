# Standard Library
from typing import Any, List

# First Party
from minislite.tables import TableManager
from minislite.exceptions import AreYouSure, AlreadyExistsError, RecordNotFoundError


class Objects:
    table_name = None
    unique_together = None

    klass: Any
    manager: Any

    def __get__(self, instance, owner):
        self.table_name = owner.get_table_name()
        self.unique_together = owner.get_unique_together()
        self.klass = owner
        self.manager = TableManager(table_name=self.table_name)

        return self

    def get(self, **kwargs) -> Any:
        db_object = self.manager.select(**kwargs).fetchone()
        if not db_object:
            raise RecordNotFoundError("This row not found.")

        dict_object = dict(db_object)
        return self.klass(**dict_object)

    def filter(self, **kwargs) -> List[Any]:
        db_objects = self.manager.select(**kwargs).fetchall()

        object_list = [self.klass(**dict(i)) for i in db_objects]
        return object_list

    def all(self) -> List[Any]:
        return self.filter()

    def first(self):
        return self.get(order_by="id", limit=1)

    def last(self):
        return self.get(order_by="-id", limit=1)

    def check_unique_together(self, is_creating=False, object_id=None, **kwargs) -> bool:
        if not self.unique_together:
            return True
        fields = {}
        for unique in self.unique_together:
            fields[unique] = kwargs.get(unique, None)

        if is_creating:
            check = self.filter(**fields)
            if check:
                return False
            return True

        db_object = self.filter(**fields)
        if db_object:
            if db_object[0].id != object_id:
                return False
        return True

    def update(self, *args, **kwargs):
        if self.check_unique_together(*args, **kwargs):
            self.manager.update(*args, **kwargs)
        else:
            raise AlreadyExistsError("This object already exists.")

    def create(self, *args, **kwargs):
        if self.check_unique_together(*args, is_creating=True, **kwargs):  # type: ignore
            object_id = self.manager.insert(*args, **kwargs)
            return self.get(id=object_id)

        raise AlreadyExistsError("This object already exists.")

    def delete(self, i_am_sure=None, object_id=None) -> None:
        if object_id is None and i_am_sure is None:
            raise AreYouSure("Cleaning all data in tables. Are you sure? Use 'i_am_sure=True'")

        self.manager.delete(object_id)
