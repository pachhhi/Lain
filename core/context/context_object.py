from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ContextObject:
    prompt: str
    intent: Optional[str] = None
    flags: Optional[Any] = None
    providers: Optional[list] = None

    # futuro (no lo uses aún)
    memory: Optional[str] = None
    session: Optional[dict] = None
    metadata: Optional[dict] = None