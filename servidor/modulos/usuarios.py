import hashlib
from .. import database


def hash_password(password: str) -> str:
    """
    Retorna o hash SHA256 da senha informada.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verificar_senha(password: str, hashed_password: str) -> bool:
    """
    Valida a senha informada comparando-a com o hash armazenado.
    """
    return hash_password(password) == hashed_password


def autenticar_usuario(usuario, senha):
    """
    Autentica um usuário com base no nome de usuário e senha.

    Args:
        usuario (str): Nome de usuário.
        senha (str): Senha em texto plano.

    Returns:
        dict: Um dicionário com o status da autenticação e o perfil do usuário se for bem-sucedido.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT senha, perfil FROM usuarios WHERE usuario = ?", (usuario,))
    user_db = cursor.fetchone()
    conn.close()

    if user_db and verificar_senha(senha, user_db["senha"]):
        return {"autenticado": True, "perfil": user_db["perfil"]}

    return {"autenticado": False, "perfil": None}

def criar_usuario(dados_usuario):
    """
    Cria um novo usuário no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)", 
                   (dados_usuario.get("usuario"), hash_password(dados_usuario.get("senha")),
                    dados_usuario.get("perfil")))
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Usuário criado com sucesso."}

def listar_usuarios():
    """
    Retorna a lista de todos os usuários.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, perfil FROM usuarios")
    usuarios_db = cursor.fetchall()
    conn.close()

    usuarios = [dict(row) for row in usuarios_db]
    return {"status": "ok", "usuarios": usuarios}


def remover_usuario(id_usuario):
    """
    Remove um usuário do banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Usuário removido com sucesso."}
