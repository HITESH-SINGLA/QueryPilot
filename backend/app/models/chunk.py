from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """
    Smallest retrievable unit inside the system.
    """

    id: UUID = Field(default_factory=uuid4)

    document_id: UUID

    text: str

    page_number: int

    chunk_index: int

    metadata: dict = Field(default_factory=dict)

    embedding_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)