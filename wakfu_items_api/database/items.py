from typing import List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Item(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: Optional["ItemTitle"] = Relationship()
    description: Optional["ItemDescription"] = Relationship()
    definition: "ItemDefinition" = Relationship()


class ItemTitle(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="item.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


class ItemDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="item.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


class ItemDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="item.id")
    useEffects: List["UseEffects"] = Relationship()
    useCriticalEffects: List["UseCriticalEffects"] = Relationship()
    equipEffects: List["EquipEffect"] = Relationship()
    item: "ItemParameters" = Relationship()


class UseEffects(SQLModel, table=True):
    id: int = Field(primary_key=True)
    definition_id: int = Field(foreign_key="itemdefinition.id")
    effect: "ItemEffect" = Relationship()


class UseCriticalEffects(SQLModel, table=True):
    id: int = Field(primary_key=True)
    definition_id: int = Field(foreign_key="itemdefinition.id")
    effect: "ItemEffect" = Relationship()


class EquipEffect(SQLModel, table=True):
    id: int = Field(primary_key=True)
    definition_id: int = Field(foreign_key="itemdefinition.id")
    effect: "ItemEffect" = Relationship()


class ItemEffect(SQLModel, table=True):
    id: int = Field(primary_key=True)
    useEffects_id: Optional[int] = Field(foreign_key="useeffects.id")
    useCriticalEffects_id: Optional[int] = Field(foreign_key="usecriticaleffects.id")
    equipEffects_id: Optional[int] = Field(foreign_key="equipeffect.id")
    definition: "EffectDefinition" = Relationship()
    description: Optional["EffectDescription"] = Relationship()


class EffectDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True)
    effect_id: int = Field(foreign_key="itemeffect.id")
    actionId: int = Field(foreign_key="action.id")
    areaShape: int
    areaSize: List[int] = Field(sa_column=Column(JSON))
    params: List[float] = Field(sa_column=Column(JSON))


class EffectDescription(SQLModel, table=True):
    id: int = Field(primary_key=True)
    effect_id: Optional[int] = Field(foreign_key="itemeffect.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


class ItemParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemdefinition.id")
    baseParameters: "BaseParameters" = Relationship()
    useParameters: "UseParameters" = Relationship()
    graphicParameters: "GraphicParameters" = Relationship()
    properties: List[int] = Field(sa_column=Column(JSON))
    level: int


class BaseParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemparameters.id")
    itemTypeId: int = Field(foreign_key="itemtype.id")
    itemSetId: int
    rarity: int
    bindType: int
    minimumShardSlotNumber: int
    maximumShardSlotNumber: int


class UseParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemparameters.id")
    useCostAp: int
    useCostMp: int
    useCostWp: int
    useRangeMin: int
    useRangeMax: int
    useTestFreeCell: bool
    useTestLos: bool
    useTestOnlyLine: bool
    useTestNoBorderCell: bool
    useWorldTarget: int


class GraphicParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemparameters.id")
    gfxId: int
    femaleGfxId: int


# TODO(Jules): Revoir cette fonction, elle est incomplete
def create_item_from_dict(data: dict) -> Item:
    """
    Crée un objet Item à partir d'un dictionnaire, robuste aux champs manquants.
    """
    id = data["definition"]["item"]["id"]

    title = ItemTitle(id=id, **data["title"]) if "title" in data else None

    description = (
        ItemDescription(id=id, **data["description"]) if "description" in data else None
    )

    return Item(
        id=id,
        title=title,
        description=description,
    )
