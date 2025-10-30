# Lista para armazenar as atividades em memória
ATIVIDADES = []

# Contador para gerar IDs únicos para as atividades
proximo_id_atividade = 1

def enviar_atividade(dados_atividade):
    """
    Envia uma nova atividade e a adiciona à lista de atividades.

    Args:
        dados_atividade (dict): Dicionário com os dados da atividade (id_turma, nome, etc.).

    Returns:
        dict: Dicionário com o status da operação e os dados da atividade enviada.
    """
    global proximo_id_atividade
    
    nova_atividade = {
        "id": proximo_id_atividade,
        "id_turma": dados_atividade.get("id_turma"),
        "nome": dados_atividade.get("nome"),
        "conteudo": dados_atividade.get("conteudo")
    }
    
    ATIVIDADES.append(nova_atividade)
    proximo_id_atividade += 1
    
    return {"status": "ok", "atividade": nova_atividade}

def listar_atividades_turma(id_turma):
    """
    Retorna a lista de todas as atividades de uma determinada turma.

    Args:
        id_turma (int): ID da turma.

    Returns:
        dict: Dicionário com o status da operação e a lista de atividades.
    """
    atividades_turma = [atividade for atividade in ATIVIDADES if atividade["id_turma"] == id_turma]
    return {"status": "ok", "atividades": atividades_turma}

def baixar_atividade(id_atividade):
    """
    Retorna o conteúdo de uma atividade.

    Args:
        id_atividade (int): ID da atividade.

    Returns:
        dict: Dicionário com o status da operação e o conteúdo da atividade.
    """
    for atividade in ATIVIDADES:
        if atividade["id"] == id_atividade:
            return {"status": "ok", "conteudo": atividade["conteudo"]}
    return {"status": "erro", "message": "Atividade não encontrada."}
