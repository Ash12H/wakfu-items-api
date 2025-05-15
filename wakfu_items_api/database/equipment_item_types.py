from typing import List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class EquipmentItemType(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    parentId: int
    equipmentPositions: List[str] = Field(sa_column=Column(JSON))
    equipmentDisabledPositions: List[str] = Field(sa_column=Column(JSON))
    isRecyclable: bool
    isVisibleInAnimation: bool
    title: Optional["EquipmentItemTypeTitle"] = Relationship()


class EquipmentItemTypeTitle(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="equipmentitemtype.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


def create_equipment_item_type_from_dict(data: dict) -> EquipmentItemType:
    title_data = data.get("title", {})
    definition = data.get("definition", {})
    return EquipmentItemType(
        id=definition["id"],
        parentId=definition["parentId"],
        equipmentPositions=definition.get("equipmentPositions", []),
        equipmentDisabledPositions=definition.get("equipmentDisabledPositions", []),
        isRecyclable=definition.get("isRecyclable", False),
        isVisibleInAnimation=definition.get("isVisibleInAnimation", False),
        title=EquipmentItemTypeTitle(
            id=definition["id"],
            fr=title_data.get("fr"),
            en=title_data.get("en"),
            es=title_data.get("es"),
            pt=title_data.get("pt"),
        ),
    )
