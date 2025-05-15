from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class ItemProperty(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    description: str


def create_item_property_from_dict(data: dict) -> ItemProperty:
    """
    Create an ItemProperty object from a dictionary.
    """
    item_property = ItemProperty(
        id=data["id"], name=data["name"], description=data["description"]
    )
    return item_property
