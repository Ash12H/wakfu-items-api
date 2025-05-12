from typing import List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class EquipmentItemType(SQLModel, table=True):
    """
    Represents an equipment item type in the database.
    """

    id: int = Field(primary_key=True, index=True)
    parentId: int
    equipmentPositions: List[str] = Field(sa_column=Column(JSON))
    equipmentDisabledPositions: List[str] = Field(sa_column=Column(JSON))
    isRecyclable: bool
    isVisibleInAnimation: bool
    title: "EquipmentItemTypeTitle" = Relationship()


class EquipmentItemTypeTitle(SQLModel, table=True):
    """
    Represents the title of an equipment item type in the database.
    """

    id: int = Field(primary_key=True, index=True, foreign_key="equipmentitemtype.id")
    fr: Optional[str]
    en: Optional[str]
    de: Optional[str]
    es: Optional[str]


def create_equipment_item_type_from_dict(data: dict) -> EquipmentItemType:
    """
    Create an Action object from a dictionary.
    """
    return EquipmentItemType(
        id=data["definition"]["id"],
        parentId=data["definition"]["parentId"],
        equipmentPositions=data["definition"]["equipmentPositions"],
        equipmentDisabledPositions=data["definition"]["equipmentDisabledPositions"],
        isRecyclable=data["definition"]["isRecyclable"],
        isVisibleInAnimation=data["definition"]["isVisibleInAnimation"],
        title=EquipmentItemTypeTitle(
            fr=data["title"].get("fr"),
            en=data["title"].get("en"),
            de=data["title"].get("de"),
            es=data["title"].get("es"),
        ),
    )
