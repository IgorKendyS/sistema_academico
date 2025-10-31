import sqlite3

DATABASE_FILE = "sistema_academico.db"

def get_db_connection():
    """
    Cria uma conexão com o banco de dados.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa o banco de dados, criando as tabelas se não existirem.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Criar tabela de turmas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            professor TEXT
        )
    """)

    # Criar tabela de alunos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL UNIQUE
        )
    """)

    # Criar tabela de aulas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turma INTEGER NOT NULL,
            data TEXT NOT NULL,
            topico TEXT NOT NULL,
            FOREIGN KEY (id_turma) REFERENCES turmas (id)
        )
    """)

    # Criar tabela de atividades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turma INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            arquivo BLOB,
            FOREIGN KEY (id_turma) REFERENCES turmas (id)
        )
    """)

    # Criar tabela de usuarios
    cursor.execute(""""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)

    # Inserir usuários dummy se não existirem
    cursor.execute("SELECT * FROM usuarios")
    if not cursor.fetchall():
        cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)", ("admin", "admin", "administrador"))
        cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)", ("prof", "prof", "professor"))
        cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)", ("aluno", "aluno", "aluno"))

    conn.commit()
    conn.close()
