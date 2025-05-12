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
    Creates an Item instance from a dictionary. This function processes
    the data received from the JSON file provided by the Wakfu team and
    maps it to the corresponding SQLModel objects.
    """
    item = Item(
        id=data["definition"]["item"]["id"],
        title=ItemTitle(
            fr=data.get("title", {}).get("fr"),
            en=data.get("title", {}).get("en"),
            es=data.get("title", {}).get("es"),
            pt=data.get("title", {}).get("pt"),
        ),
        description=ItemDescription(
            fr=data.get("description", {}).get("fr"),
            en=data.get("description", {}).get("en"),
            es=data.get("description", {}).get("es"),
            pt=data.get("description", {}).get("pt"),
        ),
        definition=ItemDefinition(
            useEffects=[
                UseEffects(
                    effect=ItemEffect(
                        description=EffectDescription(**effect.get("description", {}))
                    )
                )
                for effect in data.get("definition", {}).get("useEffects", [])
            ],
            useCriticalEffects=[
                UseCriticalEffects(
                    effect=ItemEffect(
                        description=EffectDescription(**effect.get("description", {}))
                    )
                )
                for effect in data.get("definition", {}).get("useCriticalEffects", [])
            ],
            equipEffects=[
                EquipEffect(
                    effect=ItemEffect(
                        description=EffectDescription(**effect.get("description", {}))
                    )
                )
                for effect in data.get("definition", {}).get("equipEffects", [])
            ],
            item=ItemParameters(
                baseParameters=BaseParameters(
                    **data.get("definition", {})
                    .get("item", {})
                    .get("baseParameters", {})
                ),
                useParameters=UseParameters(
                    **data.get("definition", {})
                    .get("item", {})
                    .get("useParameters", {})
                ),
                graphicParameters=GraphicParameters(
                    **data.get("definition", {})
                    .get("item", {})
                    .get("graphicParameters", {})
                ),
                properties=data.get("definition", {})
                .get("item", {})
                .get("properties", []),
            ),
        ),
    )

    return item
