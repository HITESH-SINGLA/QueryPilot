from pydantic import BaseModel, Field


class AskResponse(BaseModel):

    answer: str

    artifacts: list[str] = Field(default_factory=list)