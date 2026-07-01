from dataclasses import dataclass
from typing import Optional, Any
from typing import List, Dict, Any, Literal

Message = Dict[str, str]

@dataclass
class ContextObject:
    user_input: str
    intent: str | None = None
    mode: Optional[str] = None 
    flags: Any = None
    providers: list | None = None

    def __post_init__(self):
        assert isinstance(self.user_input, str), "user_input must be str"