from pydantic import BaseModel, RootModel
from typing import Optional


class MultiLang(BaseModel):
    fr: str = ""
    en: str = ""
    es: str = ""
    pt: str = ""


Title = MultiLang
Description = MultiLang


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
    areaSize: list[int]
    params: list[float]


class Effect(BaseModel):
    definition: EffectDefinition
    description: Optional[Description] = None


class EquipEffect(BaseModel):
    effect: Effect


class UseEffects(BaseModel):
    effect: Effect


class UseCriticalEffects(BaseModel):
    effect: Effect


class ItemParameter(BaseModel):
    id: int
    level: int
    baseParameters: BaseParameters
    useParameters: UseParameters
    graphicParameters: GraphicParameters
    properties: list[int]


class Definition(BaseModel):
    item: ItemParameter
    useEffects: list[UseEffects]
    useCriticalEffects: list[UseCriticalEffects]
    equipEffects: list[EquipEffect]


class Item(BaseModel):
    definition: Definition
    title: Optional[Title] = None
    description: Optional[Description] = None


class ItemFile(RootModel):
    root: list[Item]
