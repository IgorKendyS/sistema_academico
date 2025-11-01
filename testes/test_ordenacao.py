import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from servidor.modulos import ordenacao


def test_sort_int_array():
    assert ordenacao.sort_int_array([3, 1, 2]) == [1, 2, 3]
    assert ordenacao.sort_int_array([]) == []


def test_binary_search():
    dados = [1, 4, 6, 8, 10]
    assert ordenacao.binary_search(dados, 6) == 2
    assert ordenacao.binary_search(dados, 5) == -1
