from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Action(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    effect: str
    description: Optional["ActionDescription"] = Relationship(back_populates="action")

    @classmethod
    def from_wakfu_api(cls, data: dict) -> "Action":
        """Create an Action object from a dictionary."""
        definition = data.get("definition", {})
        description_data = data.get("description", {})
        action_id = definition.get("id")
        effect = definition.get("effect", "")

        action_description = None
        if description_data:
            action_description = ActionDescription(
                id=action_id,
                fr=description_data.get("fr"),
                en=description_data.get("en"),
                es=description_data.get("es"),
                pt=description_data.get("pt"),
            )

        return cls(
            id=action_id,
            effect=effect,
            description=action_description,
        )


class ActionDescription(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, foreign_key="action.id")
    fr: Optional[str]
    en: Optional[str]
    es: Optional[str]
    pt: Optional[str]
    action: Optional[Action] = Relationship(back_populates="description")
