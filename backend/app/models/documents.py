from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

#Class to define the structure of a Document object, which represents an original source document before chunking. It includes fields for metadata such as title, source, subject, chapter, author, publisher, edition, total pages, and creation timestamp.
class Document(BaseModel):
    """
    Represents an original source document before chunking.
    """

    id: UUID = Field(default_factory=uuid4)

    title: str

    source: str

    subject: Optional[str] = None

    chapter: Optional[str] = None

    author: Optional[str] = None

    publisher: Optional[str] = None

    edition: Optional[str] = None

    total_pages: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)