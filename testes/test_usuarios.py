import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from servidor.modulos import usuarios


def test_hash_password_produces_sha256():
    senha = "segredo"
    hash_1 = usuarios.hash_password(senha)
    hash_2 = usuarios.hash_password(senha)

    assert hash_1 == hash_2
    assert len(hash_1) == 64
    assert all(char in "0123456789abcdef" for char in hash_1)


def test_autenticar_usuario_sucesso():
    with patch("servidor.database.get_db_connection") as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        hashed = usuarios.hash_password("senha")
        mock_cursor.fetchone.return_value = {"senha": hashed, "perfil": "administrador"}

        resultado = usuarios.autenticar_usuario("admin", "senha")

        assert resultado["autenticado"] is True
        assert resultado["perfil"] == "administrador"
        mock_conn.close.assert_called_once()


def test_autenticar_usuario_falha():
    with patch("servidor.database.get_db_connection") as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        hashed = usuarios.hash_password("senha")
        mock_cursor.fetchone.return_value = {"senha": hashed, "perfil": "administrador"}

        resultado = usuarios.autenticar_usuario("admin", "senha_incorreta")

        assert resultado["autenticado"] is False
        assert resultado["perfil"] is None
        mock_conn.close.assert_called_once()
