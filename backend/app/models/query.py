from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Query(BaseModel):
    """
    User query entering the retrieval engine.
    """

    id: UUID = Field(default_factory=uuid4)

    text: str

    standalone_query: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)