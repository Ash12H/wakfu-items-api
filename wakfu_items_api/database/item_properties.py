from sqlmodel import Field, SQLModel


class ItemProperty(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    description: str

    @classmethod
    def from_wakfu_api(cls, data: dict) -> "ItemProperty":
        return cls.model_validate(data)
