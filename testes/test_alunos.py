import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from servidor.modulos import alunos

@pytest.fixture
def mock_db():
    """
    Fixture to mock the database connection.
    """
    with patch('servidor.database.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_cursor

def test_criar_aluno(mock_db):
    """
    Testa a função de criar aluno.
    """
    mock_db.lastrowid = 1
    dados_aluno = {"nome": "Aluno Teste", "matricula": "12345"}
    
    resultado = alunos.criar_aluno(dados_aluno)
    
    assert resultado["status"] == "ok"
    assert resultado["aluno"]["id"] == 1
    assert resultado["aluno"]["nome"] == "Aluno Teste"
    mock_db.execute.assert_called_once_with("INSERT INTO alunos (nome, matricula) VALUES (?, ?)", ("Aluno Teste", "12345"))

def test_listar_alunos(mock_db):
    """
    Testa a função de listar alunos.
    """
    mock_db.fetchall.return_value = [
        {"id": 1, "nome": "Aluno A", "matricula": "111"},
        {"id": 2, "nome": "Aluno B", "matricula": "222"}
    ]
    
    resultado = alunos.listar_alunos()
    
    assert resultado["status"] == "ok"
    assert len(resultado["alunos"]) == 2
    assert resultado["alunos"][0]["nome"] == "Aluno A"
    mock_db.execute.assert_called_once_with("SELECT * FROM alunos")

def test_buscar_aluno_existente(mock_db):
    """
    Testa a busca de um aluno existente utilizando o módulo em C para busca binária.
    """
    mock_db.fetchall.return_value = [{"id": 1}, {"id": 2}]
    mock_db.fetchone.return_value = {"id": 2, "nome": "Aluno B", "matricula": "222"}

    resultado = alunos.buscar_aluno(2)

    # Primeiro SELECT busca os IDs, o segundo traz os dados completos
    assert mock_db.execute.call_args_list[0][0][0] == "SELECT id FROM alunos"
    assert mock_db.execute.call_args_list[1][0][0] == "SELECT * FROM alunos WHERE id = ?"
    assert resultado["nome"] == "Aluno B"

def test_buscar_aluno_inexistente(mock_db):
    """
    Testa a busca de um aluno inexistente.
    """
    mock_db.fetchall.return_value = [{"id": 1}, {"id": 2}]

    resultado = alunos.buscar_aluno(5)

    # Apenas a consulta de IDs é realizada, pois a busca retorna -1
    mock_db.execute.assert_called_once_with("SELECT id FROM alunos")
    assert resultado is None


