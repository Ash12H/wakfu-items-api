from typing import List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Item(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: Optional["Title"] = Relationship()
    description: Optional["ItemDescription"] = Relationship()
    definition: "Definition" = Relationship()


class Title(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    item_id: int = Field(foreign_key="item.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


class ItemDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    item_id: Optional[int] = Field(foreign_key="item.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


class Definition(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    item_id: int = Field(foreign_key="item.id")
    useEffects: List["UseEffects"] = Relationship()
    useCriticalEffects: List["UseCriticalEffects"] = Relationship()
    equipEffects: List["EquipEffect"] = Relationship()
    item: "ItemParameters" = Relationship()


class UseEffects(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    definition_id: int = Field(foreign_key="definition.id")
    effect: "Effect" = Relationship()


class UseCriticalEffects(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    definition_id: int = Field(foreign_key="definition.id")
    effect: "Effect" = Relationship()


class EquipEffect(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    definition_id: int = Field(foreign_key="definition.id")
    effect: "Effect" = Relationship()


class Effect(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    useEffects_id: Optional[int] = Field(foreign_key="useeffects.id")
    useCriticalEffects_id: Optional[int] = Field(foreign_key="usecriticaleffects.id")
    equipEffects_id: Optional[int] = Field(foreign_key="equipeffect.id")
    definition: "EffectDefinition" = Relationship()
    description: Optional["EffectDescription"] = Relationship()


class EffectDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    effect_id: int = Field(foreign_key="effect.id")
    actionId: int
    areaShape: int
    areaSize: List[int] = Field(sa_column=Column(JSON))
    params: List[float] = Field(sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True


class EffectDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    effect_id: Optional[int] = Field(foreign_key="effect.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


class ItemParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    definition_id: int = Field(foreign_key="definition.id")
    baseParameters: "BaseParameters" = Relationship()
    useParameters: "UseParameters" = Relationship()
    graphicParameters: "GraphicParameters" = Relationship()
    properties: List[int] = Field(sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True


class BaseParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    itemParameters_id: int = Field(foreign_key="itemparameters.id")
    itemTypeId: int
    itemSetId: int
    rarity: int
    bindType: int
    minimumShardSlotNumber: int
    maximumShardSlotNumber: int


class UseParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    itemParameters_id: int = Field(foreign_key="itemparameters.id")
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
    id: int = Field(primary_key=True, index=True)
    itemParameters_id: int = Field(foreign_key="itemparameters.id")
    gfxId: int
    femaleGfxId: int
