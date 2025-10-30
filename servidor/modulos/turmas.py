from .ordenacao import sort_int_array

# Lista para armazenar as turmas em memória
TURMAS = []

# Contador para gerar IDs únicos para as turmas
proximo_id_turma = 1

def criar_turma(dados_turma):
    """
    Cria uma nova turma e a adiciona à lista de turmas.

    Args:
        dados_turma (dict): Dicionário com os dados da turma (nome, professor, etc.).

    Returns:
        dict: Dicionário com o status da operação e os dados da turma criada.
    """
    global proximo_id_turma
    
    novo_id = dados_turma.get("id", proximo_id_turma)

    nova_turma = {
        "id": novo_id,
        "nome": dados_turma.get("nome"),
        "professor": dados_turma.get("professor")
    }
    
    TURMAS.append(nova_turma)
    if novo_id >= proximo_id_turma:
        proximo_id_turma = novo_id + 1
    
    return {"status": "ok", "turma": nova_turma}

def listar_turmas(ordenar_por_id=False):
    """
    Retorna a lista de todas as turmas cadastradas.

    Args:
        ordenar_por_id (bool): Se True, ordena a lista de turmas por ID.

    Returns:
        dict: Dicionário com o status da operação e a lista de turmas.
    """
    if ordenar_por_id:
        print(f"TURMAS antes da ordenação: {TURMAS}")
        ids = [turma["id"] for turma in TURMAS]
        print(f"IDs: {ids}")
        sorted_ids = sort_int_array(ids)
        print(f"IDs ordenados: {sorted_ids}")
        turmas_map = {turma["id"]: turma for turma in TURMAS}
        print(f"Mapa de turmas: {turmas_map}")
        sorted_turmas = [turmas_map[id] for id in sorted_ids]
        print(f"Turmas ordenadas: {sorted_turmas}")
        return {"status": "ok", "turmas": sorted_turmas}
    else:
        return {"status": "ok", "turmas": TURMAS}

def buscar_turma(id_turma):
    """
    Busca uma turma pelo seu ID.

    Args:
        id_turma (int): ID da turma a ser buscada.

    Returns:
        dict or None: Dicionário com os dados da turma se encontrada, senão None.
    """
    for turma in TURMAS:
        if turma["id"] == id_turma:
            return turma
    return None

def atualizar_turma(id_turma, dados_turma):
    """
    Atualiza os dados de uma turma.

    Args:
        id_turma (int): ID da turma a ser atualizada.
        dados_turma (dict): Dicionário com os novos dados da turma.

    Returns:
        dict: Dicionário com o status da operação.
    """
    turma = buscar_turma(id_turma)
    if turma:
        turma.update(dados_turma)
        return {"status": "ok", "message": "Turma atualizada com sucesso."}
    else:
        return {"status": "erro", "message": "Turma não encontrada."}

def remover_turma(id_turma):
    """
    Remove uma turma da lista.

    Args:
        id_turma (int): ID da turma a ser removida.

    Returns:
        dict: Dicionário com o status da operação.
    """
    turma = buscar_turma(id_turma)
    if turma:
        TURMAS.remove(turma)
        return {"status": "ok", "message": "Turma removida com sucesso."}
    else:
        return {"status": "erro", "message": "Turma não encontrada."}
