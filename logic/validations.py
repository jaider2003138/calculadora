from .exceptions import MatrixError

# Validaciones básicas

def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_positive_int(value, name="valor"):
    if not isinstance(value, int):
        raise MatrixError(f"{name} debe ser un entero.")
    if value <= 0:
        raise MatrixError(f"{name} debe ser mayor que 0.")
    return value


def validate_matrix(M, name="A"):
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
            raise MatrixError(f"{name} debe ser rectangular.")

        new_row = []
        for j, val in enumerate(row):
            if not is_number(val):
                raise MatrixError(f"{name}[{i+1}][{j+1}] debe ser numérico.")
            new_row.append(float(val))
        out.append(new_row)

    return out


def shape(A):
    return len(A), len(A[0])


def require_same_shape(A, B, op_name="operación"):
    if shape(A) != shape(B):
        raise MatrixError(
            f"{op_name}: dimensiones incompatibles {shape(A)} vs {shape(B)}."
        )


def require_square(A, name="A"):
    r, c = shape(A)
    if r != c:
        raise MatrixError(f"{name} debe ser cuadrada, pero es {r}x{c}.")


def require_matmul_compatible(A, B):
    ar, ac = shape(A)
    br, bc = shape(B)
    if ac != br:
        raise MatrixError(
            f"Producto A·B incompatible: A es {ar}x{ac} y B es {br}x{bc}."
        )