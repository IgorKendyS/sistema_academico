# Lista para armazenar os alunos em memória
ALUNOS = []

# Contador para gerar IDs únicos para os alunos
proximo_id_aluno = 1

def criar_aluno(dados_aluno):
    """
    Cria um novo aluno e o adiciona à lista de alunos.

    Args:
        dados_aluno (dict): Dicionário com os dados do aluno (nome, matricula, etc.).

    Returns:
        dict: Dicionário com o status da operação e os dados do aluno criado.
    """
    global proximo_id_aluno
    
    novo_aluno = {
        "id": proximo_id_aluno,
        "nome": dados_aluno.get("nome"),
        "matricula": dados_aluno.get("matricula")
    }
    
    ALUNOS.append(novo_aluno)
    proximo_id_aluno += 1
    
    return {"status": "ok", "aluno": novo_aluno}

def listar_alunos():
    """
    Retorna a lista de todos os alunos cadastrados.

    Returns:
        dict: Dicionário com o status da operação e a lista de alunos.
    """
    return {"status": "ok", "alunos": ALUNOS}

def buscar_aluno(id_aluno):
    """
    Busca um aluno pelo seu ID.

    Args:
        id_aluno (int): ID do aluno a ser buscado.

    Returns:
        dict or None: Dicionário com os dados do aluno se encontrado, senão None.
    """
    for aluno in ALUNOS:
        if aluno["id"] == id_aluno:
            return aluno
    return None

def atualizar_aluno(id_aluno, dados_aluno):
    """
    Atualiza os dados de um aluno.

    Args:
        id_aluno (int): ID do aluno a ser atualizado.
        dados_aluno (dict): Dicionário com os novos dados do aluno.

    Returns:
        dict: Dicionário com o status da operação.
    """
    aluno = buscar_aluno(id_aluno)
    if aluno:
        aluno.update(dados_aluno)
        return {"status": "ok", "message": "Aluno atualizado com sucesso."}
    else:
        return {"status": "erro", "message": "Aluno não encontrado."}

def remover_aluno(id_aluno):
    """
    Remove um aluno da lista.

    Args:
        id_aluno (int): ID do aluno a ser removido.

    Returns:
        dict: Dicionário com o status da operação.
    """
    aluno = buscar_aluno(id_aluno)
    if aluno:
        ALUNOS.remove(aluno)
        return {"status": "ok", "message": "Aluno removido com sucesso."}
    else:
        return {"status": "erro", "message": "Aluno não encontrado."}
