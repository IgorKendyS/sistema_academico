import ctypes
from pathlib import Path

LIB_PATH = Path(__file__).resolve().parents[2] / "c_module" / "modulos.so"
lib = ctypes.CDLL(str(LIB_PATH))

# Define os tipos de argumento e retorno das funções em C
lib.sort_array.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
lib.sort_array.restype = None

lib.binary_search.argtypes = (
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int,
    ctypes.c_int,
)
lib.binary_search.restype = ctypes.c_int


def sort_int_array(arr):
    """
    Ordena uma lista de inteiros usando a função C.

    Args:
        arr (list[int]): Lista de inteiros a ser ordenada.

    Returns:
        list[int]: A lista ordenada.
    """
    if not arr:
        return []

    n = len(arr)
    c_array = (ctypes.c_int * n)(*arr)
    lib.sort_array(c_array, n)
    return list(c_array)


def binary_search(sorted_arr, target):
    """
    Executa busca binária em um array ordenado utilizando o módulo em C.

    Args:
        sorted_arr (list[int]): Lista de inteiros ordenada em ordem crescente.
        target (int): Valor a ser buscado.

    Returns:
        int: Índice do elemento encontrado ou -1 se não existir.
    """
    if not sorted_arr:
        return -1

    n = len(sorted_arr)
    c_array = (ctypes.c_int * n)(*sorted_arr)
    return lib.binary_search(c_array, n, target)
