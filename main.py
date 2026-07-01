#Que deberia tener main.py?

# UI de consola
# ↓
# recibir input
# ↓
# enviar a run_lain()
# ↓
# mostrar respuesta
# ↓
# guardar logs

from tools.run_lain import run_lain
from core.helpers.logger import write_log
from core.helpers.ui import type_text


def main():
    print("Lain v1]")
    print("Escribí 'exit' para salir.\n")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            print("Adiós!")
            break

        write_log("USER", user_input)

        response = run_lain(user_input)        
        
        type_text(response)

        write_log("ASSISTANT", response)


if __name__ == "__main__":
    main()