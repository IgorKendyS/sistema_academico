# Lista para armazenar as aulas em memória
AULAS = []

# Contador para gerar IDs únicos para as aulas
proximo_id_aula = 1

def registrar_aula(dados_aula):
    """
    Registra uma nova aula e a adiciona à lista de aulas.

    Args:
        dados_aula (dict): Dicionário com os dados da aula (id_turma, conteudo, etc.).

    Returns:
        dict: Dicionário com o status da operação e os dados da aula registrada.
    """
    global proximo_id_aula
    
    nova_aula = {
        "id": proximo_id_aula,
        "id_turma": dados_aula.get("id_turma"),
        "conteudo": dados_aula.get("conteudo"),
        "data": dados_aula.get("data")
    }
    
    AULAS.append(nova_aula)
    proximo_id_aula += 1
    
    return {"status": "ok", "aula": nova_aula}

def listar_aulas_turma(id_turma):
    """
    Retorna a lista de todas as aulas de uma determinada turma.

    Args:
        id_turma (int): ID da turma.

    Returns:
        dict: Dicionário com o status da operação e a lista de aulas.
    """
    aulas_turma = [aula for aula in AULAS if aula["id_turma"] == id_turma]
    return {"status": "ok", "aulas": aulas_turma}
