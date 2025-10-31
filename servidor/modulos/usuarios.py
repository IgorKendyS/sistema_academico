import hashlib
from .. import database

# TODO: Hash passwords before storing them in the database.

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
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    user_db = cursor.fetchone()
    conn.close()
    
    if user_db:
        return {"autenticado": True, "perfil": user_db["perfil"]}
    else:
        return {"autenticado": False, "perfil": None}