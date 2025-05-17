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

    @classmethod
    def from_wakfu_api(cls, data: dict) -> "ItemType":
        definition = data.get("definition", {})
        title_data = data.get("title", {})
        item_type_id = definition.get("id")

        item_type_title = None
        if title_data:
            item_type_title = ItemTypeTitle(
                id=item_type_id,
                fr=title_data.get("fr"),
                en=title_data.get("en"),
                es=title_data.get("es"),
                pt=title_data.get("pt"),
            )

        return cls(
            id=item_type_id,
            parentId=definition.get("parentId"),
            equipmentPositions=definition.get("equipmentPositions", []),
            equipmentDisabledPositions=definition.get("equipmentDisabledPositions", []),
            isRecyclable=definition.get("isRecyclable", False),
            isVisibleInAnimation=definition.get("isVisibleInAnimation", False),
            title=item_type_title,
        )


class ItemTypeTitle(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="itemtype.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]
