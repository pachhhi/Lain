from pathlib import Path
import json
from core.helpers.memory_helpers import *

class MemoryProvider:

    def get_context(self, prompt=None):
        return load_memory()