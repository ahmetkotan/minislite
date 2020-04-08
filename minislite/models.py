# Standard Library
from typing import List

# First Party
from minislite.fields import DatabaseField
from minislite.tables import TableManager
from minislite.objects import Objects


class MiniLiteModel:
    id = DatabaseField(field_type=int, auto_increment=True)

    table_name = None
    unique_together: List[str] = []
    objects = Objects()

    def __init__(self, **kwargs):
        self.reload_attributes(**kwargs)
        self.manager = TableManager(table_name=self.get_table_name())

    def reload_attributes(self, **kwargs) -> None:
        field_list = self.get_fields()
        for field in field_list:
            exists_attr = getattr(self, field, None)
            if isinstance(exists_attr, DatabaseField):
                exists_attr = exists_attr.default
            value = kwargs.get(field, exists_attr)
            setattr(self, field, value)

        setattr(self, "id", kwargs.get("id", None))

    def save(self):
        field_list = self.get_fields()
        fields = {}
        for field in field_list:
            fields[field] = getattr(self, field, None)

        if not self.id:
            this_object = self.objects.create(**fields)
            self.id = this_object.id
        else:
            self.objects.update(object_id=self.id, **fields)

    def delete(self):
        if self.id:
            self.objects.delete(self.id)
            self.id = None  # type: ignore

    @classmethod
    def get_unique_together(cls) -> List[str]:
        return cls.unique_together

    @classmethod
    def get_table_name(cls) -> str:
        table_name = cls.table_name
        if table_name is None:
            table_name = cls.__name__.lower()
        return table_name

    @classmethod
    def get_fields(cls) -> List[str]:
        field_list = []
        for (field, value) in cls.__dict__.items():
            if isinstance(value, DatabaseField):
                field_list.append(field)

        return field_list
