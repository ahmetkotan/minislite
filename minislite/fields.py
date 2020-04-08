class DatabaseField:
    def __init__(self, field_type, default=None, unique=False, not_null=True, auto_increment=False) -> None:
        self.field_type = field_type
        self.default = default
        self.not_null = not_null
        self.unique = unique
        self.auto_increment = auto_increment
