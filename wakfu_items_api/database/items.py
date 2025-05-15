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
    actionId: int
    areaShape: int
    areaSize: List[int] = Field(sa_column=Column(JSON))
    params: List[float] = Field(sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True


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

    class Config:
        arbitrary_types_allowed = True


class BaseParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemparameters.id")
    itemTypeId: int
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


def create_item_from_dict(data: dict) -> Item:
    """
    Crée un objet Item à partir d'un dictionnaire, robuste aux champs manquants.
    """
    title_data = data.get("title", {})
    desc_data = data.get("description", {})
    definition = data.get("definition", {})
    item_data = definition.get("item", {})

    # Sous-objets de paramètres
    base_params = item_data.get("baseParameters", {})
    use_params = item_data.get("useParameters", {})
    graphic_params = item_data.get("graphicParameters", {})

    # Création de l'objet Item
    item = Item(
        id=item_data.get("id", None),
        title=ItemTitle(
            fr=title_data.get("fr"),
            en=title_data.get("en"),
            es=title_data.get("es"),
            pt=title_data.get("pt"),
        )
        if title_data
        else None,
        description=ItemDescription(
            fr=desc_data.get("fr"),
            en=desc_data.get("en"),
            es=desc_data.get("es"),
            pt=desc_data.get("pt"),
        )
        if desc_data
        else None,
        definition=ItemDefinition(
            useEffects=[
                UseEffects(
                    effect=ItemEffect(
                        description=EffectDescription(**effect.get("description", {}))
                    )
                )
                for effect in definition.get("useEffects", []) or []
            ],
            useCriticalEffects=[
                UseCriticalEffects(
                    effect=ItemEffect(
                        description=EffectDescription(**effect.get("description", {}))
                    )
                )
                for effect in definition.get("useCriticalEffects", []) or []
            ],
            equipEffects=[
                EquipEffect(
                    effect=ItemEffect(
                        description=EffectDescription(**effect.get("description", {}))
                    )
                )
                for effect in definition.get("equipEffects", []) or []
            ],
            item=ItemParameters(
                baseParameters=BaseParameters(**base_params) if base_params else None,
                useParameters=UseParameters(**use_params) if use_params else None,
                graphicParameters=GraphicParameters(**graphic_params)
                if graphic_params
                else None,
                properties=item_data.get("properties", []),
            )
            if item_data
            else None,
        )
        if definition
        else None,
    )
    return item
