import tkinter as tk
from tkinter import ttk, messagebox
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


class MatrixApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora de Matrices")
        self.root.geometry("1250x780")
        self.root.configure(bg="#cfefff")

        self.entries_A = []
        self.entries_B = []

        self.create_widgets()
    # UI
    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Calculadora de Matrices",
            font=("Segoe UI", 28, "bold"),
            bg="#cfefff",
            fg="#003366"
        )
        title.pack(pady=25)

        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)

        ttk.Label(top_frame, text="Operación:").grid(row=0, column=0, padx=8)

        self.operation = ttk.Combobox(
            top_frame,
            state="readonly",
            width=22,
            values=[
                "Sumar",
                "Restar",
                "Multiplicar",
                "Dividir",
                "Sumar Escalar",
                "Restar Escalar",
                "Multiplicar Escalar",
                "Dividir Escalar",
                "Determinante",
                "Inversa",
                "Transpuesta",
                "Traza"
            ]
        )
        self.operation.grid(row=0, column=1, padx=8)
        self.operation.bind("<<ComboboxSelected>>", self.update_visibility)

        ttk.Label(top_frame, text="Filas:").grid(row=0, column=2, padx=8)
        self.rows = ttk.Entry(top_frame, width=6)
        self.rows.grid(row=0, column=3, padx=8)

        ttk.Label(top_frame, text="Columnas:").grid(row=0, column=4, padx=8)
        self.cols = ttk.Entry(top_frame, width=6)
        self.cols.grid(row=0, column=5, padx=8)

        ttk.Button(top_frame, text="Generar", command=self.generate_matrices).grid(row=0, column=6, padx=12)
        ttk.Button(top_frame, text="Llenar Aleatorio", command=self.fill_random).grid(row=0, column=7, padx=12)

        # Campo escalar
        self.scalar_label = ttk.Label(top_frame, text="Escalar k:")
        self.scalar_entry = ttk.Entry(top_frame, width=8)

        # Contenedor matrices
        matrix_container = ttk.Frame(self.root)
        matrix_container.pack(pady=30)

        self.frame_A = ttk.LabelFrame(matrix_container, text="Matriz A")
        self.frame_A.grid(row=0, column=0, padx=60)

        self.frame_B = ttk.LabelFrame(matrix_container, text="Matriz B")
        self.frame_B.grid(row=0, column=1, padx=60)

        # Botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Calcular", command=self.calculate).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="Nueva Operación", command=self.reset_all).grid(row=0, column=1, padx=15)
        ttk.Button(button_frame, text="Salir", command=self.root.destroy).grid(row=0, column=2, padx=15)

        self.result_frame = ttk.LabelFrame(self.root, text="Resultado")
        self.result_frame.pack(pady=25)

    # VISIBILIDAD DINÁMICA
    def update_visibility(self, event=None):
        op = self.operation.get()

        # Operaciones con dos matrices
        if op in ["Sumar", "Restar", "Multiplicar", "Dividir"]:
            self.frame_B.grid()
        else:
            self.frame_B.grid_remove()

        # Operaciones escalares
        if "Escalar" in op:
            self.scalar_label.grid(row=0, column=8, padx=6)
            self.scalar_entry.grid(row=0, column=9, padx=6)
        else:
            self.scalar_label.grid_remove()
            self.scalar_entry.grid_remove()

    # =========================
    # GENERAR MATRICES
    # =========================
    def generate_matrices(self):
        for frame in [self.frame_A, self.frame_B, self.result_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        self.entries_A = []
        self.entries_B = []

        try:
            r = int(self.rows.get())
            c = int(self.cols.get())
        except ValueError:
            messagebox.showerror("Error", "Dimensiones inválidas")
            return

        for i in range(r):
            rowA = []
            rowB = []
            for j in range(c):
                eA = ttk.Entry(self.frame_A, width=8, font=("Segoe UI", 12))
                eA.grid(row=i, column=j, padx=4, pady=4)
                rowA.append(eA)

                eB = ttk.Entry(self.frame_B, width=8, font=("Segoe UI", 12))
                eB.grid(row=i, column=j, padx=4, pady=4)
                rowB.append(eB)

            self.entries_A.append(rowA)
            self.entries_B.append(rowB)

    # LLENAR ALEATORIO
    def fill_random(self):
        for row in self.entries_A:
            for e in row:
                e.delete(0, tk.END)
                e.insert(0, random.randint(-10, 10))

        for row in self.entries_B:
            for e in row:
                e.delete(0, tk.END)
                e.insert(0, random.randint(-10, 10))

    def get_matrix(self, entries):
        return [[float(e.get()) for e in row] for row in entries]

    # MOSTRAR RESULTADO
    def show_result_matrix(self, matrix):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if isinstance(matrix, list):
            for i, row in enumerate(matrix):
                for j, val in enumerate(row):
                    lbl = tk.Label(
                        self.result_frame,
                        text=round(val, 2),
                        font=("Segoe UI", 13, "bold"),
                        bg="#e6f7ff",
                        width=7
                    )
                    lbl.grid(row=i, column=j, padx=6, pady=6)
        else:
            tk.Label(
                self.result_frame,
                text=round(matrix, 4),
                font=("Segoe UI", 16, "bold"),
                bg="#e6f7ff",
                width=12
            ).pack(pady=10)

    # CALCULAR
    def calculate(self):
        try:
            op = self.operation.get()
            A = self.get_matrix(self.entries_A)

            if op in ["Sumar", "Restar", "Multiplicar", "Dividir"]:
                B = self.get_matrix(self.entries_B)

            if "Escalar" in op:
                k = float(self.scalar_entry.get())

            if op == "Sumar":
                result = sumar_matrices(A, B)
            elif op == "Restar":
                result = restar_matrices(A, B)
            elif op == "Multiplicar":
                result = multiplicar_matrices(A, B)
            elif op == "Dividir":
                result = dividir_matrices(A, B)
            elif op == "Sumar Escalar":
                result = sumar_escalar(A, k)
            elif op == "Restar Escalar":
                result = restar_escalar(A, k)
            elif op == "Multiplicar Escalar":
                result = multiplicar_escalar(A, k)
            elif op == "Dividir Escalar":
                result = dividir_escalar(A, k)
            elif op == "Determinante":
                result = calcular_determinante(A)
            elif op == "Inversa":
                result = calcular_matriz_inversa(A)
            elif op == "Transpuesta":
                result = calcular_transpuesta(A)
            elif op == "Traza":
                result = calcular_traza(A)
            else:
                messagebox.showwarning("Aviso", "Seleccione una operación")
                return

            self.show_result_matrix(result)

        except MatrixError as e:
            messagebox.showerror("Error", str(e))
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos")

    def reset_all(self):
        self.rows.delete(0, tk.END)
        self.cols.delete(0, tk.END)
        self.scalar_entry.delete(0, tk.END)
        self.operation.set("")

        for frame in [self.frame_A, self.frame_B, self.result_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        self.entries_A = []
        self.entries_B = []

    def run(self):
        self.root.mainloop()