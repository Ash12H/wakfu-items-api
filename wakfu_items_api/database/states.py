from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class State(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: Optional["StateDescription"] = Relationship(back_populates="state")


class StateDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="state.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]
    state: Optional[State] = Relationship(back_populates="title")


def create_state_from_dict(data: dict) -> State:
    """
    Crée un objet State à partir d'un dictionnaire.
    """
    title_data = data.get("title", {})
    state = State(
        id=data["definition"]["id"],
        title=StateDescription(
            id=data["definition"]["id"],
            fr=title_data.get("fr"),
            en=title_data.get("en"),
            es=title_data.get("es"),
            pt=title_data.get("pt"),
        )
        if title_data
        else None,
    )
    return state
