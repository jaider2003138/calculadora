# ==========================================
#  CALCULADORA DE MATRICES (MENÚ)
import random

# -------------------------
# Errores personalizados
# -------------------------
class MatrixError(Exception):
    """Error para validaciones y operaciones de matrices."""
    pass


# -------------------------
# Validaciones básicas
# -------------------------
def is_number(x):
    """True si x es int/float (y no bool)."""
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_positive_int(value, name="valor"):
    """Valida que sea entero > 0."""
    if not isinstance(value, int):
        raise MatrixError(f"{name} debe ser un entero.")
    if value <= 0:
        raise MatrixError(f"{name} debe ser mayor que 0.")
    return value


def validate_matrix(M, name="A"):
    """
    Valida que M sea una matriz rectangular con números.
    Retorna una copia en float.
    """
    if not isinstance(M, list) or len(M) == 0:
        raise MatrixError(f"{name} debe ser una lista no vacía de filas.")

    cols = None
    out = []

    for i, row in enumerate(M):
        if not isinstance(row, list) or len(row) == 0:
            raise MatrixError(f"{name}: la fila {i+1} debe ser una lista no vacía.")

        if cols is None:
            cols = len(row)
        elif len(row) != cols:
            raise MatrixError(f"{name} debe ser rectangular: todas las filas con la misma cantidad de columnas.")

        new_row = []
        for j, val in enumerate(row):
            if not is_number(val):
                raise MatrixError(f"{name}[{i+1}][{j+1}] debe ser numérico (int/float).")
            new_row.append(float(val))
        out.append(new_row)

    return out


def shape(A):
    """Retorna (filas, columnas). A debe estar validada."""
    return len(A), len(A[0])


def require_same_shape(A, B, op_name="operación"):
    """Valida mismas dimensiones para suma/resta/hadamard/div elem a elem."""
    if shape(A) != shape(B):
        raise MatrixError(f"{op_name}: dimensiones incompatibles {shape(A)} vs {shape(B)}.")


def require_square(A, name="A"):
    """Valida que sea cuadrada para determinante, inversa, traza, adjunta."""
    r, c = shape(A)
    if r != c:
        raise MatrixError(f"{name} debe ser cuadrada, pero es {r}x{c}.")


def require_matmul_compatible(A, B):
    """
    Regla del producto matricial:
    Si A es (m x n) y B es (p x q), se puede multiplicar si n == p.
    Resultado será (m x q).
    """
    ar, ac = shape(A)
    br, bc = shape(B)
    if ac != br:
        raise MatrixError(f"Producto A·B incompatible: A es {ar}x{ac} y B es {br}x{bc}. Debe cumplirse columnas(A) == filas(B).")


# -------------------------
# Utilidades
# -------------------------
def transpose(A):
    """Transpuesta de A."""
    r, c = shape(A)
    return [[A[i][j] for i in range(r)] for j in range(c)]


def print_matrix(M, title="Resultado"):
    """Imprime una matriz con formato."""
    print(f"\n{title}:")
    for row in M:
        print("  ", " ".join(f"{v:.6g}" for v in row))


# -------------------------
# Entrada segura (evitar strings donde van números)
# -------------------------
def read_int_strict(prompt):
    """
    Lee un entero.
    - No permite string no numérico.
    - Acepta negativos si el usuario escribe -3 (por si los necesitas en rangos).
    """
    s = input(prompt).strip()
    if s == "":
        raise MatrixError("Entrada vacía. Debes escribir un número entero.")

    # Validación manual (sin librerías)
    # Permitimos signo al inicio
    if s[0] == "-":
        if len(s) == 1 or not s[1:].isdigit():
            raise MatrixError("Debes escribir un entero válido (ej: -3, 0, 12).")
    else:
        if not s.isdigit():
            raise MatrixError("Debes escribir un entero válido (ej: 0, 12, 25).")

    return int(s)


def read_float_strict(prompt):
    """
    Lee un float.
    - No permite texto.
    - Permite enteros y decimales, con signo.
    Ej: 3, -2, 4.5, -0.25
    """
    s = input(prompt).strip()
    if s == "":
        raise MatrixError("Entrada vacía. Debes escribir un número.")

    # Validación manual: permitir un solo punto y un signo al inicio
    # Reglas:
    #  - puede empezar con '-'
    #  - máximo 1 punto '.'
    #  - el resto deben ser dígitos
    if s[0] == "-":
        body = s[1:]
        if body == "":
            raise MatrixError("Debes escribir un número válido.")
    else:
        body = s

    parts = body.split(".")
    if len(parts) > 2:
        raise MatrixError("Número inválido: tiene más de un punto decimal.")

    # Debe haber dígitos en al menos una parte
    if len(parts) == 1:
        if not parts[0].isdigit():
            raise MatrixError("Número inválido. Ejemplos: 3, -2, 4.5")
    else:
        left, right = parts[0], parts[1]
        # permitir ".5" ? aquí NO, exigimos al menos un dígito a la izquierda
        if left == "" or not left.isdigit():
            raise MatrixError("Número inválido. Ejemplos: 4.5, -0.25")
        if right == "" or not right.isdigit():
            raise MatrixError("Número inválido. Ejemplos: 4.5, -0.25")

    return float(s)


def read_positive_int(prompt, name="valor"):
    """Lee un entero > 0 (para filas/columnas)."""
    x = read_int_strict(prompt)
    validate_positive_int(x, name)
    return x


# -------------------------
# Lectura de matrices (manual o aleatoria)
# -------------------------
def read_matrix_manual(name="A"):
    """
    Permite ingresar manualmente la matriz.
    Valida filas/columnas y que cada fila tenga la cantidad correcta de valores numéricos.
    """
    print(f"\n--- Matriz {name} (MANUAL) ---")
    r = read_positive_int("Número de filas: ", "filas")
    c = read_positive_int("Número de columnas: ", "columnas")

    M = []
    for i in range(r):
        while True:
            row_str = input(f"Fila {i+1} (exactamente {c} valores separados por espacios): ").strip()
            parts = row_str.split()

            if len(parts) != c:
                print(f"Error: debes ingresar EXACTAMENTE {c} valores.")
                continue

            # convertir cada valor a float con validación estricta
            row = []
            ok = True
            for p in parts:
                try:
                    # Validación estricta: reutilizamos lógica simple
                    # (aquí usamos float(), pero antes filtramos casos obvios de texto)
                    # Si p contiene letras, float fallará.
                    val = float(p)
                except:
                    ok = False
                    break
                row.append(val)

            if not ok:
                print("Error: todos los valores deben ser numéricos (ej: 1, -2, 3.5).")
                continue

            M.append(row)
            break

    return validate_matrix(M, name=name)


def read_matrix_random(name="A"):
    """
    Genera una matriz aleatoria.
    - El usuario elige tipo: enteros o decimales
    - Elige rango [min, max]
    """
    print(f"\n--- Matriz {name} (ALEATORIA) ---")
    r = read_positive_int("Número de filas: ", "filas")
    c = read_positive_int("Número de columnas: ", "columnas")

    print("\nTipo de números aleatorios:")
    print("1) Enteros")
    print("2) Decimales")
    t = input("Elige (1/2): ").strip()

    low = read_int_strict("Valor mínimo (entero): ")
    high = read_int_strict("Valor máximo (entero): ")

    if low > high:
        raise MatrixError("El mínimo no puede ser mayor que el máximo.")

    match t:
        case "1":
            # randint incluye ambos extremos
            M = [[float(random.randint(low, high)) for _ in range(c)] for _ in range(r)]
        case "2":
            # random.random() -> [0, 1)
            # escalamos a [low, high]
            if low == high:
                # todos serán el mismo número
                M = [[float(low) for _ in range(c)] for _ in range(r)]
            else:
                M = []
                for _ in range(r):
                    row = []
                    for _ in range(c):
                        x = low + (high - low) * random.random()
                        row.append(float(x))
                    M.append(row)
        case _:
            raise MatrixError("Opción inválida. Debes elegir 1 o 2.")

    return validate_matrix(M, name=name)


def choose_matrix(name="A"):
    """Permite elegir si la matriz se ingresa manual o aleatoria."""
    print(f"\n¿Cómo quieres obtener la matriz {name}?")
    print("1) Ingresar manualmente")
    print("2) Generar aleatoria")
    choice = input("Elige (1/2): ").strip()

    match choice:
        case "1":
            return read_matrix_manual(name)
        case "2":
            return read_matrix_random(name)
        case _:
            raise MatrixError("Opción inválida al crear matriz.")


# -------------------------
# Operaciones con escalar
# -------------------------
def scalar_op(A, k, op):
    """
    A op k:
    1) suma A + k
    2) resta A - k
    3) multiplicación A * k
    4) división A / k
    """
    A = validate_matrix(A, "A")

    if not is_number(k):
        raise MatrixError("El escalar k debe ser numérico (int/float).")
    k = float(k)

    match op:
        case "1":
            return [[v + k for v in row] for row in A]
        case "2":
            return [[v - k for v in row] for row in A]
        case "3":
            return [[v * k for v in row] for row in A]
        case "4":
            if k == 0.0:
                raise MatrixError("No se puede dividir por escalar 0.")
            return [[v / k for v in row] for row in A]
        case _:
            raise MatrixError("Opción inválida para operación con escalar.")


# -------------------------
# Operaciones entre matrices
# -------------------------
def elementwise(A, B, op_name):
    """Suma/resta/hadamard/división elemento a elemento."""
    require_same_shape(A, B, op_name)

    r, c = shape(A)

    def calc(x, y):
        match op_name:
            case "add":
                return x + y
            case "sub":
                return x - y
            case "mul":
                return x * y
            case "div":
                if y == 0.0:
                    raise MatrixError("División elemento a elemento: se encontró un 0 en la matriz B.")
                return x / y
            case _:
                raise MatrixError("Operación elemento a elemento inválida.")

    return [[calc(A[i][j], B[i][j]) for j in range(c)] for i in range(r)]


def matmul(A, B):
    """Producto matricial A·B con validación de dimensiones."""
    require_matmul_compatible(A, B)

    ar, ac = shape(A)
    br, bc = shape(B)

    # Para optimizar, usamos la transpuesta de B
    Bt = transpose(B)
    out = []

    for i in range(ar):
        row = []
        for j in range(bc):
            s = 0.0
            for k in range(ac):
                s += A[i][k] * Bt[j][k]
            row.append(s)
        out.append(row)

    return out


def matrix_op(A, B, op):
    """
    Operaciones entre matrices:
    1) suma
    2) resta
    3) división elemento a elemento
    4) hadamard
    5) producto matricial
    """
    A = validate_matrix(A, "A")
    B = validate_matrix(B, "B")

    match op:
        case "1":
            return elementwise(A, B, "add")
        case "2":
            return elementwise(A, B, "sub")
        case "3":
            return elementwise(A, B, "div")
        case "4":
            return elementwise(A, B, "mul")
        case "5":
            return matmul(A, B)
        case _:
            raise MatrixError("Opción inválida para operación entre matrices.")


# -------------------------
# Determinante, Adjunta, Inversa, Traza, Transpuesta
# -------------------------
def determinant(A):
    """
    Determinante por eliminación Gaussiana con pivoteo parcial.
    Valida cuadrada.
    """
    A = validate_matrix(A, "A")
    require_square(A, "A")

    n, _ = shape(A)
    M = [row[:] for row in A]  # copia

    det = 1.0
    sign = 1.0

    for col in range(n):
        # Buscar pivote (fila con mayor valor absoluto en la columna)
        pivot = col
        max_abs = M[col][col]
        if max_abs < 0:
            max_abs = -max_abs

        for r in range(col + 1, n):
            v = M[r][col]
            if v < 0:
                v = -v
            if v > max_abs:
                max_abs = v
                pivot = r

        # Si el pivote es 0, determinante es 0
        if max_abs == 0.0:
            return 0.0

        # Intercambio de filas cambia el signo del determinante
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            sign *= -1.0

        pivot_val = M[col][col]
        det *= pivot_val

        # Eliminación hacia abajo
        for r in range(col + 1, n):
            factor = M[r][col] / pivot_val
            if factor != 0.0:
                for c in range(col, n):
                    M[r][c] -= factor * M[col][c]

    return det * sign


def minor_matrix(A, row_remove, col_remove):
    """Construye el menor eliminando fila row_remove y columna col_remove."""
    n, m = shape(A)
    out = []

    for i in range(n):
        if i == row_remove:
            continue
        row = []
        for j in range(m):
            if j == col_remove:
                continue
            row.append(A[i][j])
        out.append(row)

    return out


def adjugate(A):
    """
    Matriz adjunta = Transpuesta de la matriz de cofactores.
    Valida cuadrada.
    """
    A = validate_matrix(A, "A")
    require_square(A, "A")

    n, _ = shape(A)

    if n == 1:
        return [[1.0]]

    cof = []
    for i in range(n):
        row = []
        for j in range(n):
            Mn = minor_matrix(A, i, j)
            c = determinant(Mn)
            if (i + j) % 2 == 1:
                c = -c
            row.append(c)
        cof.append(row)

    return transpose(cof)


def trace(A):
    """Traza: suma de la diagonal. Valida cuadrada."""
    A = validate_matrix(A, "A")
    require_square(A, "A")

    n, _ = shape(A)
    s = 0.0
    for i in range(n):
        s += A[i][i]
    return s


def inverse(A):
    """
    Inversa por Gauss-Jordan con pivoteo parcial.
    Valida cuadrada y no singular.
    """
    A = validate_matrix(A, "A")
    require_square(A, "A")

    n, _ = shape(A)

    # Matriz aumentada [A | I]
    aug = []
    for i in range(n):
        row = A[i][:] + [0.0] * n
        row[n + i] = 1.0
        aug.append(row)

    for col in range(n):
        # buscar pivote
        pivot = col
        max_abs = aug[col][col]
        if max_abs < 0:
            max_abs = -max_abs

        for r in range(col + 1, n):
            v = aug[r][col]
            if v < 0:
                v = -v
            if v > max_abs:
                max_abs = v
                pivot = r

        if max_abs == 0.0:
            raise MatrixError("La matriz es singular (det=0). No tiene inversa.")

        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]

        pivot_val = aug[col][col]

        # Normalizar fila pivote para que el pivote sea 1
        for c in range(2 * n):
            aug[col][c] = aug[col][c] / pivot_val

        # Hacer ceros en las demás filas
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor != 0.0:
                for c in range(2 * n):
                    aug[r][c] = aug[r][c] - factor * aug[col][c]

    # Extraer la parte derecha (inversa)
    inv = []
    for i in range(n):
        inv.append(aug[i][n:])
    return inv


def unary_op(A, op):
    """
    Operaciones unarias:
    1) det
    2) adjunta
    3) inversa
    4) traza
    5) transpuesta
    """
    match op:
        case "1":
            return determinant(A)
        case "2":
            return adjugate(A)
        case "3":
            return inverse(A)
        case "4":
            return trace(A)
        case "5":
            A2 = validate_matrix(A, "A")
            return transpose(A2)
        case _:
            raise MatrixError("Opción inválida para operación unaria.")


# -------------------------
# Menú principal con validaciones
# -------------------------
def main_menu():
    while True:
        print("\n==============================")
        print("   CALCULADORA DE MATRICES")
        print("==============================")
        print("1) Operaciones con escalar (una matriz)")
        print("2) Operaciones entre matrices")
        print("3) Determinante / Adjunta / Inversa / Traza / Transpuesta")
        print("0) Salir")

        op = input("Elige una opción (0-3): ").strip()

        match op:
            case "0":
                print("Saliendo...")
                return

            case "1":
                try:
                    A = choose_matrix("A")
                    print("\nOperaciones con escalar:")
                    print("1) Suma (A + k)")
                    print("2) Resta (A - k)")
                    print("3) Multiplicación (A * k)")
                    print("4) División (A / k)")
                    o = input("Elige (1-4): ").strip()

                    # Aquí validamos que k sea numérico (no texto)
                    k = read_float_strict("Ingresa el escalar k (número): ")

                    R = scalar_op(A, k, o)
                    print_matrix(R, "Resultado")

                except Exception as e:
                    print(f"Error: {e}")

            case "2":
                try:
                    A = choose_matrix("A")
                    B = choose_matrix("B")

                    print("\nOperaciones entre matrices:")
                    print("1) Suma (A + B)                 -> requiere mismas dimensiones")
                    print("2) Resta (A - B)                -> requiere mismas dimensiones")
                    print("3) División elemento a elemento -> requiere mismas dimensiones y B sin ceros")
                    print("4) Hadamard (A ⊙ B)             -> requiere mismas dimensiones")
                    print("5) Producto matricial (A · B)   -> requiere columnas(A) == filas(B)")
                    o = input("Elige (1-5): ").strip()

                    R = matrix_op(A, B, o)
                    print_matrix(R, "Resultado")

                except Exception as e:
                    print(f"Error: {e}")

            case "3":
                try:
                    A = choose_matrix("A")

                    print("\nOperaciones unarias:")
                    print("1) Determinante det(A)   -> requiere matriz cuadrada")
                    print("2) Matriz adjunta adj(A) -> requiere matriz cuadrada")
                    print("3) Inversa inv(A)        -> requiere cuadrada y no singular")
                    print("4) Traza tr(A)           -> requiere matriz cuadrada")
                    print("5) Transpuesta A^T       -> cualquier matriz")
                    o = input("Elige (1-5): ").strip()

                    R = unary_op(A, o)

                    # Si R es matriz, imprimimos como matriz; si no, es número
                    if isinstance(R, list):
                        print_matrix(R, "Resultado")
                    else:
                        print(f"\nResultado: {R:.6g}")

                except Exception as e:
                    print(f"Error: {e}")

            case _:
                print("Opción inválida. Debes elegir 0, 1, 2 o 3.")


if __name__ == "__main__":
    main_menu()
