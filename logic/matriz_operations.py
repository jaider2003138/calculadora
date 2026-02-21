from .exceptions import MatrixError
from .validations import (
    validate_matrix,
    shape,
    require_same_shape,
    require_square,
    require_matmul_compatible
)

# OPERACIONES ENTRE MATRICES
def calcular_transpuesta(A):
    A = validate_matrix(A, "A")
    r, c = shape(A)
    return [[A[i][j] for i in range(r)] for j in range(c)]


def sumar_matrices(A, B):
    A = validate_matrix(A, "A")
    B = validate_matrix(B, "B")
    require_same_shape(A, B, "Suma")

    r, c = shape(A)
    return [[A[i][j] + B[i][j] for j in range(c)] for i in range(r)]


def restar_matrices(A, B):
    A = validate_matrix(A, "A")
    B = validate_matrix(B, "B")
    require_same_shape(A, B, "Resta")

    r, c = shape(A)
    return [[A[i][j] - B[i][j] for j in range(c)] for i in range(r)]


def multiplicar_matrices(A, B):
    A = validate_matrix(A, "A")
    B = validate_matrix(B, "B")
    require_matmul_compatible(A, B)

    ar, ac = shape(A)
    br, bc = shape(B)

    Bt = calcular_transpuesta(B)
    resultado = []

    for i in range(ar):
        fila = []
        for j in range(bc):
            suma = 0.0
            for k in range(ac):
                suma += A[i][k] * Bt[j][k]
            fila.append(suma)
        resultado.append(fila)

    return resultado

def dividir_matrices(A, B):
    """
    División de matrices:
    A / B  =  A * B⁻¹
    """

    A = validate_matrix(A, "A")
    B = validate_matrix(B, "B")

    require_square(B, "B")

    inversa_B = calcular_matriz_inversa(B)

    return multiplicar_matrices(A, inversa_B)

# OPERACIONES ESCALARES

def sumar_escalar(A, k):
    """
    A + k
    """
    A = validate_matrix(A, "A")

    if not isinstance(k, (int, float)):
        raise MatrixError("El escalar debe ser un número.")

    r, c = shape(A)
    return [[A[i][j] + k for j in range(c)] for i in range(r)]


def restar_escalar(A, k):
    """
    A - k
    """
    A = validate_matrix(A, "A")

    if not isinstance(k, (int, float)):
        raise MatrixError("El escalar debe ser un número.")

    r, c = shape(A)
    return [[A[i][j] - k for j in range(c)] for i in range(r)]


def multiplicar_escalar(A, k):
    """
    A * k
    """
    A = validate_matrix(A, "A")

    if not isinstance(k, (int, float)):
        raise MatrixError("El escalar debe ser un número.")

    r, c = shape(A)
    return [[A[i][j] * k for j in range(c)] for i in range(r)]


def dividir_escalar(A, k):
    """
    A / k
    """
    A = validate_matrix(A, "A")

    if not isinstance(k, (int, float)):
        raise MatrixError("El escalar debe ser un número.")

    if k == 0:
        raise MatrixError("No se puede dividir por cero.")

    r, c = shape(A)
    return [[A[i][j] / k for j in range(c)] for i in range(r)]


# DETERMINANTE

def calcular_determinante(A):

    A = validate_matrix(A, "A")
    require_square(A, "A")

    n, _ = shape(A)
    M = [row[:] for row in A]

    determinante = 1.0
    signo = 1.0

    for col in range(n):

        fila_pivote = col
        max_abs = abs(M[col][col])

        for r in range(col + 1, n):
            if abs(M[r][col]) > max_abs:
                max_abs = abs(M[r][col])
                fila_pivote = r

        if max_abs == 0.0:
            return 0.0

        if fila_pivote != col:
            M[col], M[fila_pivote] = M[fila_pivote], M[col]
            signo *= -1.0

        pivote = M[col][col]
        determinante *= pivote

        for r in range(col + 1, n):
            factor = M[r][col] / pivote
            for c in range(col, n):
                M[r][c] -= factor * M[col][c]

    return determinante * signo

# INVERSA
def calcular_matriz_inversa(A):

    A = validate_matrix(A, "A")
    require_square(A, "A")

    n, _ = shape(A)

    M = [row[:] for row in A]
    I = [[float(i == j) for j in range(n)] for i in range(n)]

    for col in range(n):

        fila_pivote = col
        max_abs = abs(M[col][col])

        for r in range(col + 1, n):
            if abs(M[r][col]) > max_abs:
                max_abs = abs(M[r][col])
                fila_pivote = r

        if max_abs == 0.0:
            raise MatrixError("La matriz no es invertible (determinante = 0).")

        if fila_pivote != col:
            M[col], M[fila_pivote] = M[fila_pivote], M[col]
            I[col], I[fila_pivote] = I[fila_pivote], I[col]

        pivote = M[col][col]

        for j in range(n):
            M[col][j] /= pivote
            I[col][j] /= pivote

        for r in range(n):
            if r != col:
                factor = M[r][col]
                for j in range(n):
                    M[r][j] -= factor * M[col][j]
                    I[r][j] -= factor * I[col][j]

    return I


# TRAZA

def calcular_traza(A):
    A = validate_matrix(A, "A")
    require_square(A, "A")

    n, _ = shape(A)
    return sum(A[i][i] for i in range(n))