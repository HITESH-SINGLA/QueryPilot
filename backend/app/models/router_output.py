from pydantic import BaseModel


class RouterOutput(BaseModel):

    requires_retrieval: bool

    requires_python: bool

    requires_web: bool

    requires_multi_hop: bool

    reasoning: str