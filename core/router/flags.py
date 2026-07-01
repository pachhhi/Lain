from dataclasses import dataclass
from typing import Optional


@dataclass
class Flags:
    language: str = "auto"
    verbosity: str = "normal"   # low | normal | high
    use_memory: bool = False
    use_history: bool = False
    summarize_history: bool = False