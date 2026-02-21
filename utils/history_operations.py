from datetime import datetime
import os

HISTORY_FILE = "historial.txt"


def formatear_matriz(matriz):
    return "\n".join(
        ["\t".join(f"{valor:.2f}" for valor in fila) for fila in matriz]
    )


def guardar_operacion(operacion, A, B=None, escalar=None, resultado=None):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crear archivo si no existe
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("HISTORIAL DE OPERACIONES\n")
            f.write("=" * 60 + "\n\n")

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Fecha: {fecha}\n")
        f.write(f"Operación: {operacion}\n\n")

        f.write("Matriz A:\n")
        f.write(formatear_matriz(A) + "\n\n")

        if B is not None:
            f.write("Matriz B:\n")
            f.write(formatear_matriz(B) + "\n\n")

        if escalar is not None:
            f.write(f"Escalar k: {escalar}\n\n")

        f.write("Resultado:\n")

        if isinstance(resultado, list):
            f.write(formatear_matriz(resultado) + "\n")
        else:
            f.write(str(round(resultado, 4)) + "\n")

        f.write("\n")