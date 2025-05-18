from typing import List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Item(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: Optional["ItemTitle"] = Relationship()
    description: Optional["ItemDescription"] = Relationship()
    definition: "ItemDefinition" = Relationship()

    @classmethod
    def from_wakfu_api(cls, data: dict) -> "Item":
        """
        Create an Item instance from the Wakfu API data.
        """
        id = data["definition"]["item"]["id"]
        definition = ItemDefinition.from_wakfu_api(id=id, data=data["definition"])

        title = None
        if "title" in data:
            title = ItemTitle.from_wakfu_api(id=id, data=data["title"])

        description = None
        if "description" in data:
            description = ItemDescription.from_wakfu_api(
                id=id, data=data["description"]
            )

        return cls(id=id, title=title, description=description, definition=definition)


class ItemTitle(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="item.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "ItemTitle":
        """
        Create an ItemTitle instance from the Wakfu API data.
        """
        return cls(
            id=id,
            fr=data.get("fr"),
            en=data.get("en"),
            es=data.get("es"),
            pt=data.get("pt"),
        )


class ItemDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="item.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "ItemDescription":
        """
        Create an ItemDescription instance from the Wakfu API data.
        """
        return cls(
            id=id,
            fr=data.get("fr"),
            en=data.get("en"),
            es=data.get("es"),
            pt=data.get("pt"),
        )


class ItemDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="item.id")
    useEffects: List["UseEffects"] = Relationship()
    useCriticalEffects: List["UseCriticalEffects"] = Relationship()
    equipEffects: List["EquipEffect"] = Relationship()
    item: "ItemParameters" = Relationship()

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "ItemDefinition":
        """
        Create an ItemDefinition instance from the Wakfu API data.
        """
        useEffects = [
            UseEffects.from_wakfu_api(id=id, data=effect)
            for effect in data.get("useEffects", [])
        ]
        useCriticalEffects = [
            UseCriticalEffects.from_wakfu_api(id=id, data=effect)
            for effect in data.get("useCriticalEffects", [])
        ]
        equipEffects = [
            EquipEffect.from_wakfu_api(id=id, data=effect)
            for effect in data.get("equipEffects", [])
        ]
        item = ItemParameters.from_wakfu_api(data=data["item"])

        return cls(
            id=id,
            useEffects=useEffects,
            useCriticalEffects=useCriticalEffects,
            equipEffects=equipEffects,
            item=item,
        )


class UseEffects(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    itemdefinition_id: int = Field(foreign_key="itemdefinition.id")
    definition: "UseEffectDefinition" = Relationship()
    description: Optional["UseEffectDescription"] = Relationship()

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "UseEffects":
        """
        Create a UseEffects instance from the Wakfu API data.
        """

        definition = None
        if "definition" in data["effect"]:
            definition = UseEffectDefinition.from_wakfu_api(
                id=id, data=data["effect"].get("definition")
            )

        description = None
        if "description" in data["effect"]:
            description = UseEffectDescription.from_wakfu_api(
                id=id, data=data["effect"].get("description")
            )

        return cls(itemdefinition_id=id, definition=definition, description=description)


class UseEffectDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True)
    effect_id: int = Field(foreign_key="useeffects.id")
    actionId: int = Field(foreign_key="action.id")
    areaShape: int
    areaSize: List[int] = Field(sa_column=Column(JSON))
    params: List[float] = Field(sa_column=Column(JSON))

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "UseEffectDefinition":
        """
        Create a UseEffectDefinition instance from the Wakfu API data.
        """
        return cls(
            id=data.get("id"),
            effect_id=id,
            actionId=data.get("actionId"),
            areaShape=data.get("areaShape"),
            areaSize=data.get("areaSize"),
            params=data.get("params"),
        )


class UseEffectDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="useeffects.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "UseEffectDescription":
        """
        Create a UseEffectDescription instance from the Wakfu API data.
        """
        return cls(
            id=id,
            fr=data.get("fr"),
            en=data.get("en"),
            es=data.get("es"),
            pt=data.get("pt"),
        )


class UseCriticalEffects(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    itemdefinition_id: int = Field(foreign_key="itemdefinition.id")
    definition: "UseCriticalEffectDefinition" = Relationship()
    description: Optional["UseCriticalEffectDescription"] = Relationship()

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "UseCriticalEffects":
        """
        Create a UseCriticalEffects instance from the Wakfu API data.
        """

        definition = None
        if "definition" in data["effect"]:
            definition = UseCriticalEffectDefinition.from_wakfu_api(
                id=id, data=data["effect"].get("definition")
            )

        description = None
        if "description" in data["effect"]:
            description = UseCriticalEffectDescription.from_wakfu_api(
                id=id, data=data["effect"].get("description")
            )

        return cls(itemdefinition_id=id, definition=definition, description=description)


class UseCriticalEffectDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True)
    effect_id: int = Field(foreign_key="usecriticaleffects.id")
    actionId: int = Field(foreign_key="action.id")
    areaShape: int
    areaSize: List[int] = Field(sa_column=Column(JSON))
    params: List[float] = Field(sa_column=Column(JSON))

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "UseCriticalEffectDefinition":
        """
        Create an UseCriticalEffectDefinition instance from the Wakfu API data.
        """
        return cls(
            id=data.get("id"),
            effect_id=id,
            actionId=data.get("actionId"),
            areaShape=data.get("areaShape"),
            areaSize=data.get("areaSize"),
            params=data.get("params"),
        )


class UseCriticalEffectDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="usecriticaleffects.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "UseCriticalEffectDescription":
        """
        Create an UseCriticalEffectDescription instance from the Wakfu API data.
        """
        return cls(
            id=id,
            fr=data.get("fr"),
            en=data.get("en"),
            es=data.get("es"),
            pt=data.get("pt"),
        )


class EquipEffect(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    itemdefinition_id: int = Field(foreign_key="itemdefinition.id")
    definition: "EquipEffectDefinition" = Relationship()
    description: Optional["EquipEffectDescription"] = Relationship()

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "EquipEffect":
        """
        Create a EquipEffect instance from the Wakfu API data.
        """

        definition = None
        if "definition" in data["effect"]:
            definition = EquipEffectDefinition.from_wakfu_api(
                id=id, data=data["effect"].get("definition")
            )

        description = None
        if "description" in data["effect"]:
            description = EquipEffectDescription.from_wakfu_api(
                id=id, data=data["effect"].get("description")
            )

        return cls(itemdefinition_id=id, definition=definition, description=description)


class EquipEffectDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True)
    effect_id: int = Field(foreign_key="equipeffect.id")
    actionId: int = Field(foreign_key="action.id")
    areaShape: int
    areaSize: List[int] = Field(sa_column=Column(JSON))
    params: List[float] = Field(sa_column=Column(JSON))

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "EquipEffectDefinition":
        """
        Create an EquipEffectDefinition instance from the Wakfu API data.
        """
        return cls(
            id=data.get("id"),
            effect_id=id,
            actionId=data.get("actionId"),
            areaShape=data.get("areaShape"),
            areaSize=data.get("areaSize"),
            params=data.get("params"),
        )


class EquipEffectDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="equipeffect.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "EquipEffectDescription":
        """
        Create an EquipEffectDescription instance from the Wakfu API data.
        """
        return cls(
            id=id,
            fr=data.get("fr"),
            en=data.get("en"),
            es=data.get("es"),
            pt=data.get("pt"),
        )


class ItemParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemdefinition.id")
    baseParameters: "BaseParameters" = Relationship()
    useParameters: "UseParameters" = Relationship()
    graphicParameters: "GraphicParameters" = Relationship()
    properties: List[int] = Field(sa_column=Column(JSON))
    level: int

    @classmethod
    def from_wakfu_api(cls, data: dict) -> "ItemParameters":
        """
        Create an ItemParameters instance from the Wakfu API data.
        """
        id = data["id"]
        baseParameters = BaseParameters.from_wakfu_api(
            id=id, data=data["baseParameters"]
        )
        useParameters = UseParameters.from_wakfu_api(id=id, data=data["useParameters"])
        graphicParameters = GraphicParameters.from_wakfu_api(
            id=id, data=data["graphicParameters"]
        )

        return cls(
            id=data.get("id"),
            baseParameters=baseParameters,
            useParameters=useParameters,
            graphicParameters=graphicParameters,
            properties=data.get("properties"),
            level=data.get("level"),
        )


class BaseParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemparameters.id")
    itemTypeId: int = Field(foreign_key="itemtype.id")
    itemSetId: int
    rarity: int
    bindType: int
    minimumShardSlotNumber: int
    maximumShardSlotNumber: int

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "BaseParameters":
        """
        Create a BaseParameters instance from the Wakfu API data.
        """
        return cls(
            id=id,
            itemTypeId=data.get("itemTypeId"),
            itemSetId=data.get("itemSetId"),
            rarity=data.get("rarity"),
            bindType=data.get("bindType"),
            minimumShardSlotNumber=data.get("minimumShardSlotNumber"),
            maximumShardSlotNumber=data.get("maximumShardSlotNumber"),
        )


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

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "UseParameters":
        """
        Create a UseParameters instance from the Wakfu API data.
        """
        return cls(
            id=id,
            useCostAp=data.get("useCostAp"),
            useCostMp=data.get("useCostMp"),
            useCostWp=data.get("useCostWp"),
            useRangeMin=data.get("useRangeMin"),
            useRangeMax=data.get("useRangeMax"),
            useTestFreeCell=data.get("useTestFreeCell"),
            useTestLos=data.get("useTestLos"),
            useTestOnlyLine=data.get("useTestOnlyLine"),
            useTestNoBorderCell=data.get("useTestNoBorderCell"),
            useWorldTarget=data.get("useWorldTarget"),
        )


class GraphicParameters(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="itemparameters.id")
    gfxId: int
    femaleGfxId: int

    @classmethod
    def from_wakfu_api(cls, id: int, data: dict) -> "GraphicParameters":
        """
        Create a GraphicParameters instance from the Wakfu API data.
        """
        return cls(
            id=id,
            gfxId=data.get("gfxId"),
            femaleGfxId=data.get("femaleGfxId"),
        )
