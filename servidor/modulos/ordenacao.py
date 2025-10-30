import ctypes

# Carrega a biblioteca compartilhada
lib = ctypes.CDLL("./c_module/modulos.so")

# Define os tipos de argumento e de retorno da função C
lib.sort_array.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
lib.sort_array.restype = None

def sort_int_array(arr):
    """
    Ordena uma lista de inteiros usando a função C.

    Args:
        arr (list of int): A lista de inteiros a ser ordenada.

    Returns:
        list of int: A lista ordenada.
    """
    n = len(arr)
    c_array = (ctypes.c_int * n)(*arr)
    lib.sort_array(c_array, n)
    return list(c_array)
