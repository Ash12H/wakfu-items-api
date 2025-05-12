from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Action(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    effect: str
    description: Optional["ActionDescription"] = Relationship()


class ActionDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="action.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]


def create_action_from_dict(data: dict) -> Action:
    """
    Create an Action object from a dictionary.
    """
    action = Action(
        id=data["definition"]["id"],
        effect=data["definition"]["effect"],
        description=ActionDescription(
            fr=data["description"].get("fr"),
            en=data["description"].get("en"),
            es=data["description"].get("es"),
            pt=data["description"].get("pt"),
        )
        if "description" in data and data["description"]
        else None,
    )
    return action
