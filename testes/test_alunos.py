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



