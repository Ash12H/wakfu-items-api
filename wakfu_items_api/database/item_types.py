from typing import List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class ItemType(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    parentId: Optional[int] = Field(foreign_key="itemtype.id", nullable=True)
    equipmentPositions: List[str] = Field(sa_column=Column(JSON))
    equipmentDisabledPositions: List[str] = Field(sa_column=Column(JSON))
    isRecyclable: bool
    isVisibleInAnimation: bool
    title: Optional["ItemTypeTitle"] = Relationship()


class ItemTypeTitle(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="itemtype.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


def create_item_type_from_dict(data: dict) -> ItemType:
    title_data = data.get("title", {})
    definition = data.get("definition", {})
    return ItemType(
        id=definition["id"],
        parentId=definition.get("parentId", None),
        equipmentPositions=definition.get("equipmentPositions", []),
        equipmentDisabledPositions=definition.get("equipmentDisabledPositions", []),
        isRecyclable=definition.get("isRecyclable", False),
        isVisibleInAnimation=definition.get("isVisibleInAnimation", False),
        title=ItemTypeTitle(
            id=definition["id"],
            fr=title_data.get("fr"),
            en=title_data.get("en"),
            es=title_data.get("es"),
            pt=title_data.get("pt"),
        ),
    )
