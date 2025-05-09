from pydantic import BaseModel, RootModel
from typing import Optional, List
from pydantic import Field


class BaseParameters(BaseModel):
    itemTypeId: int
    itemSetId: int
    rarity: int
    bindType: int
    minimumShardSlotNumber: int
    maximumShardSlotNumber: int


class UseParameters(BaseModel):
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


class GraphicParameters(BaseModel):
    gfxId: int
    femaleGfxId: int


class EffectDefinition(BaseModel):
    id: int
    actionId: int
    areaShape: int
    areaSize: list
    params: list[float]


class EffectContent(BaseModel):
    definition: EffectDefinition


class Effect(BaseModel):
    effect: EffectContent


class Item(BaseModel):
    id: int
    level: int
    baseParameters: BaseParameters
    useParameters: UseParameters
    graphicParameters: GraphicParameters
    properties: list


class Definition(BaseModel):
    item: Item
    useEffects: list
    useCriticalEffects: list
    equipEffects: list[Effect]


class MultiLang(BaseModel):
    fr: str = ""
    en: str = ""
    es: str = ""
    pt: str = ""


Title = MultiLang
Description = MultiLang


class ItemSchema(BaseModel):
    definition: Definition
    title: Title = Field(default_factory=MultiLang)
    description: Description = Field(default_factory=MultiLang)


class ItemFileSchema(RootModel):
    root: list[ItemSchema]
