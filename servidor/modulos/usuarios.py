import hashlib

# Dicionário para armazenar usuários e senhas (substituir por um banco de dados em produção)
# As senhas devem ser armazenadas como hashes SHA256
USUARIOS = {
    "admin": {
        "senha": hashlib.sha256("admin123".encode()).hexdigest(),
        "perfil": "administrador"
    },
    "professor": {
        "senha": hashlib.sha256("prof123".encode()).hexdigest(),
        "perfil": "professor"
    },
    "aluno": {
        "senha": hashlib.sha256("aluno123".encode()).hexdigest(),
        "perfil": "aluno"
    }
}

def autenticar_usuario(usuario, senha):
    """
    Autentica um usuário com base no nome de usuário e senha.

    Args:
        usuario (str): Nome de usuário.
        senha (str): Senha em texto plano.

    Returns:
        dict: Um dicionário com o status da autenticação e o perfil do usuário se for bem-sucedido.
    """
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha_hash:
        return {"autenticado": True, "perfil": USUARIOS[usuario]["perfil"]}
    else:
        return {"autenticado": False, "perfil": None}
