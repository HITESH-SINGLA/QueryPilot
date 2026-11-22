from dataclasses import dataclass, field


@dataclass
class PythonResponse:

    code: str

    output: str

    artifacts: list[str] = field(default_factory=list)

    context: str = ""