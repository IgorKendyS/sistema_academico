import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from servidor.modulos import turmas

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

def test_criar_turma(mock_db):
    """
    Testa a função de criar turma.
    """
    mock_db.lastrowid = 1
    dados_turma = {"nome": "Turma Teste", "professor": "Prof. Teste"}
    
    resultado = turmas.criar_turma(dados_turma)
    
    assert resultado["status"] == "ok"
    assert resultado["turma"]["id"] == 1
    assert resultado["turma"]["nome"] == "Turma Teste"
    mock_db.execute.assert_called_once_with("INSERT INTO turmas (nome, professor) VALUES (?, ?)", ("Turma Teste", "Prof. Teste"))

def test_listar_turmas(mock_db):
    """
    Testa a função de listar turmas.
    """
    mock_db.fetchall.return_value = [
        {"id": 1, "nome": "Turma A", "professor": "Prof. A"},
        {"id": 2, "nome": "Turma B", "professor": "Prof. B"}
    ]
    
    resultado = turmas.listar_turmas()
    
    assert resultado["status"] == "ok"
    assert len(resultado["turmas"]) == 2
    assert resultado["turmas"][0]["nome"] == "Turma A"
    mock_db.execute.assert_called_once_with("SELECT * FROM turmas")

def test_buscar_turma(mock_db):
    """
    Testa a função de buscar turma.
    """
    mock_db.fetchone.return_value = {"id": 1, "nome": "Turma A", "professor": "Prof. A"}
    
    resultado = turmas.buscar_turma(1)
    
    assert resultado["id"] == 1
    assert resultado["nome"] == "Turma A"
    mock_db.execute.assert_called_once_with("SELECT * FROM turmas WHERE id = ?", (1,))

def test_atualizar_turma(mock_db):
    """
    Testa a função de atualizar turma.
    """
    mock_db.rowcount = 1
    dados_turma = {"nome": "Turma A-2", "professor": "Prof. A-2"}
    
    resultado = turmas.atualizar_turma(1, dados_turma)
    
    assert resultado["status"] == "ok"
    mock_db.execute.assert_called_once_with("UPDATE turmas SET nome = ?, professor = ? WHERE id = ?", ("Turma A-2", "Prof. A-2", 1))

def test_remover_turma(mock_db):
    """
    Testa a função de remover turma.
    """
    mock_db.rowcount = 1
    
    resultado = turmas.remover_turma(1)
    
    assert resultado["status"] == "ok"
    mock_db.execute.assert_called_once_with("DELETE FROM turmas WHERE id = ?", (1,))