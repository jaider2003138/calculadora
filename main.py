import random

from logic.matriz_operations import (
    sumar_matrices,
    restar_matrices,
    multiplicar_matrices,
    dividir_matrices,
    sumar_escalar,
    restar_escalar,
    multiplicar_escalar,
    dividir_escalar,
    calcular_determinante,
    calcular_matriz_inversa,
    calcular_transpuesta,
    calcular_traza
)

from logic.exceptions import MatrixError

# CREAR MATRIZ

def crear_matriz(nombre):
    filas = int(input(f"Ingrese número de filas de {nombre}: "))
    columnas = int(input(f"Ingrese número de columnas de {nombre}: "))

    print(f"\n¿Cómo desea llenar la matriz {nombre}?")
    print("1. Manual")
    print("2. Aleatoria")

    modo = input("Seleccione una opción: ")

    matriz = []

    if modo == "1":
        print(f"\nIngrese los valores de {nombre} fila por fila:")
        for i in range(filas):
            fila = []
            for j in range(columnas):
                valor = float(input(f"{nombre}[{i}][{j}]: "))
                fila.append(valor)
            matriz.append(fila)

    elif modo == "2":
        for i in range(filas):
            fila = []
            for j in range(columnas):
                fila.append(random.randint(-10, 10))
            matriz.append(fila)

        print(f"\nMatriz {nombre} generada automáticamente:")
        for fila in matriz:
            print(fila)

    else:
        print("Opción inválida.")
        return crear_matriz(nombre)

    return matriz


# MAIN

def main():
    while True:
        print("\n MENÚ MATRICES")
        print("1. Sumar matrices")
        print("2. Restar matrices")
        print("3. Multiplicar matrices")
        print("4. Dividir matrices (A * B⁻¹)")
        print("5. Sumar escalar (A + k)")
        print("6. Restar escalar (A - k)")
        print("7. Multiplicar escalar (A * k)")
        print("8. Dividir escalar (A / k)")
        print("9. Determinante")
        print("10. Inversa")
        print("11. Transpuesta")
        print("12. Traza")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            match opcion:

                # MATRICES

                case "1":
                    A = crear_matriz("A")
                    B = crear_matriz("B")
                    resultado = sumar_matrices(A, B)
                    print("Resultado:", resultado)

                case "2":
                    A = crear_matriz("A")
                    B = crear_matriz("B")
                    resultado = restar_matrices(A, B)
                    print("Resultado:", resultado)

                case "3":
                    A = crear_matriz("A")
                    B = crear_matriz("B")
                    resultado = multiplicar_matrices(A, B)
                    print("Resultado:", resultado)

                case "4":
                    A = crear_matriz("A")
                    B = crear_matriz("B")
                    resultado = dividir_matrices(A, B)
                    print("Resultado:", resultado)

                # ESCALARES

                case "5":
                    A = crear_matriz("A")
                    k = float(input("Ingrese el escalar k: "))
                    resultado = sumar_escalar(A, k)
                    print("Resultado:", resultado)

                case "6":
                    A = crear_matriz("A")
                    k = float(input("Ingrese el escalar k: "))
                    resultado = restar_escalar(A, k)
                    print("Resultado:", resultado)

                case "7":
                    A = crear_matriz("A")
                    k = float(input("Ingrese el escalar k: "))
                    resultado = multiplicar_escalar(A, k)
                    print("Resultado:", resultado)

                case "8":
                    A = crear_matriz("A")
                    k = float(input("Ingrese el escalar k: "))
                    resultado = dividir_escalar(A, k)
                    print("Resultado:", resultado)

                # INDIVIDUALES 

                case "9":
                    A = crear_matriz("A")
                    resultado = calcular_determinante(A)
                    print("Determinante:", resultado)

                case "10":
                    A = crear_matriz("A")
                    resultado = calcular_matriz_inversa(A)
                    print("Inversa:", resultado)

                case "11":
                    A = crear_matriz("A")
                    resultado = calcular_transpuesta(A)
                    print("Transpuesta:", resultado)

                case "12":
                    A = crear_matriz("A")
                    resultado = calcular_traza(A)
                    print("Traza:", resultado)

                case "0":
                    print("Saliendo...")
                    break

                case _:
                    print("Opción inválida")

        except MatrixError as e:
            print("Error:", e)

        except ValueError:
            print("Error: Debe ingresar valores numéricos.")

# EJECUCIÓN
from gui.app import MatrixApp
if __name__ == "__main__":
     app = MatrixApp() 
     app.run()