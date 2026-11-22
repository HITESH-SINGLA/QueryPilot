from dataclasses import dataclass


@dataclass
class RoutingDecision:
    """
    Represents the execution strategy selected
    by the LLM Router.
    """

    strategy: str
    reason: str
    confidence: float