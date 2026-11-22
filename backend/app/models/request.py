from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    uploaded_files: list[str] = []