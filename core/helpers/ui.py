#typea la response en main.py

import sys
import time

def type_text(text: str, delay: float = 0.01):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)

    print()