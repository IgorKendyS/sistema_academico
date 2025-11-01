import hashlib
import sqlite3
from pathlib import Path

DATABASE_FILENAME = "sistema_academico.db"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / DATABASE_FILENAME

DEFAULT_USERS = (
    ("admin", "admin", "administrador"),
    ("prof", "prof", "professor"),
    ("aluno", "aluno", "aluno"),
)


def _hash_password(password: str) -> str:
    """
    Retorna o hash SHA256 da senha informada.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_db_connection():
    """
    Cria uma conexão com o banco de dados.
    """
    conn = sqlite3.connect(str(DATABASE_FILE))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Inicializa o banco de dados, criando as tabelas se não existirem.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Criar tabela de turmas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            professor TEXT
        )
        """
    )

    # Criar tabela de alunos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL UNIQUE
        )
        """
    )

    # Criar tabela de aulas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS aulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turma INTEGER NOT NULL,
            data TEXT NOT NULL,
            topico TEXT NOT NULL,
            FOREIGN KEY (id_turma) REFERENCES turmas (id)
        )
        """
    )

    # Criar tabela de atividades
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turma INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            arquivo BLOB,
            FOREIGN KEY (id_turma) REFERENCES turmas (id)
        )
        """
    )

    # Criar tabela de usuarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
        """
    )

    # Inserir usuários dummy se não existirem
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        for usuario, senha, perfil in DEFAULT_USERS:
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)",
                (usuario, _hash_password(senha), perfil),
            )
    else:
        # Garante que senhas antigas em texto puro sejam convertidas para hash
        cursor.execute("SELECT id, senha FROM usuarios")
        for user_id, senha in cursor.fetchall():
            senha_str = str(senha)
            if len(senha_str) != 64 or any(
                char not in "0123456789abcdef" for char in senha_str.lower()
            ):
                cursor.execute(
                    "UPDATE usuarios SET senha = ? WHERE id = ?",
                    (_hash_password(senha_str), user_id),
                )

    conn.commit()
    conn.close()
