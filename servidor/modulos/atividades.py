from .. import database

def enviar_atividade(dados_atividade):
    """
    Envia uma nova atividade e a insere no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO atividades (id_turma, titulo, descricao, arquivo) VALUES (?, ?, ?, ?)", 
                   (dados_atividade.get("id_turma"), dados_atividade.get("titulo"), 
                    dados_atividade.get("descricao"), dados_atividade.get("arquivo")))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    
    nova_atividade = {
        "id": novo_id,
        "id_turma": dados_atividade.get("id_turma"),
        "titulo": dados_atividade.get("titulo"),
        "descricao": dados_atividade.get("descricao")
    }
    
    return {"status": "ok", "atividade": nova_atividade}

def listar_atividades_turma(id_turma):
    """
    Retorna a lista de todas as atividades de uma determinada turma.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, id_turma, titulo, descricao FROM atividades WHERE id_turma = ?", (id_turma,))
    atividades_db = cursor.fetchall()
    conn.close()

    atividades = [dict(row) for row in atividades_db]
    return {"status": "ok", "atividades": atividades}

def baixar_atividade(id_atividade):
    """
    Retorna o conteúdo de uma atividade.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT arquivo FROM atividades WHERE id = ?", (id_atividade,))
    atividade_db = cursor.fetchone()
    conn.close()
    
    if atividade_db and atividade_db["arquivo"]:
        return {"status": "ok", "arquivo": atividade_db["arquivo"]}
    else:
        return {"status": "erro", "message": "Atividade não encontrada ou sem arquivo."}

def remover_atividade(id_atividade):
    """
    Remove uma atividade do banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atividades WHERE id = ?", (id_atividade,))
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Atividade removida com sucesso."}