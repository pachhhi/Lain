import subprocess
import sys
import time

def run_llm(prompt: str, model: str = "qwen3:8b", typing: bool = True) -> str:
    proc = subprocess.Popen(
        ["ollama", "run", model, prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    output = []

    for line in proc.stdout:
        output.append(line)

        if typing:
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.0015)
        else:
            sys.stdout.write(line)
            sys.stdout.flush()

    proc.wait()
    sys.stdout.write("\n")

    return "".join(output)