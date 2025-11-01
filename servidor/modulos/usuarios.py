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
