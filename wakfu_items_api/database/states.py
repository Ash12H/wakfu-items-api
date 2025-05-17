from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class State(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: Optional["StateTitle"] = Relationship(back_populates="state")
    description: Optional["StateDescription"] = Relationship(back_populates="state")

    @classmethod
    def from_wakfu_api(cls, data: dict) -> "State":
        state_id = data.get("definition").get("id")
        title_data = data.get("title", {})
        description_data = data.get("description", {})

        state_title = None
        if title_data:
            state_title = StateTitle(
                id=state_id,
                fr=title_data.get("fr"),
                en=title_data.get("en"),
                es=title_data.get("es"),
                pt=title_data.get("pt"),
            )

        state_description = None
        if description_data:
            state_description = StateDescription(
                id=state_id,
                fr=description_data.get("fr"),
                en=description_data.get("en"),
                es=description_data.get("es"),
                pt=description_data.get("pt"),
            )

        return cls(
            id=state_id,
            title=state_title,
            description=state_description,
        )


class StateTitle(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="state.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]
    state: Optional[State] = Relationship(back_populates="title")


class StateDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="state.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]
    state: Optional[State] = Relationship(back_populates="description")
