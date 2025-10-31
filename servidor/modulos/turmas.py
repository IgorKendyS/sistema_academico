from .ordenacao import sort_int_array
from .. import database

def criar_turma(dados_turma):
    """
    Cria uma nova turma e a insere no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO turmas (nome, professor) VALUES (?, ?)", 
                   (dados_turma.get("nome"), dados_turma.get("professor")))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    
    nova_turma = {
        "id": novo_id,
        "nome": dados_turma.get("nome"),
        "professor": dados_turma.get("professor")
    }
    
    return {"status": "ok", "turma": nova_turma}

def listar_turmas(ordenar_por_id=False):
    """
    Retorna a lista de todas as turmas cadastradas no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turmas")
    turmas_db = cursor.fetchall()
    conn.close()

    turmas = [dict(row) for row in turmas_db]

    if ordenar_por_id:
        ids = [turma["id"] for turma in turmas]
        sorted_ids = sort_int_array(ids)
        turmas_map = {turma["id"]: turma for turma in turmas}
        sorted_turmas = [turmas_map[id] for id in sorted_ids]
        return {"status": "ok", "turmas": sorted_turmas}
    else:
        return {"status": "ok", "turmas": turmas}

def buscar_turma(id_turma):
    """
    Busca uma turma pelo seu ID no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turmas WHERE id = ?", (id_turma,))
    turma_db = cursor.fetchone()
    conn.close()
    
    if turma_db:
        return dict(turma_db)
    return None

def atualizar_turma(id_turma, dados_turma):
    """
    Atualiza os dados de uma turma no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE turmas SET nome = ?, professor = ? WHERE id = ?", 
                   (dados_turma.get("nome"), dados_turma.get("professor"), id_turma))
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    
    if updated_rows > 0:
        return {"status": "ok", "message": "Turma atualizada com sucesso."}
    else:
        return {"status": "erro", "message": "Turma não encontrada."}

def remover_turma(id_turma):
    """
    Remove uma turma do banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM turmas WHERE id = ?", (id_turma,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    
    if deleted_rows > 0:
        return {"status": "ok", "message": "Turma removida com sucesso."}
    else:
        return {"status": "erro", "message": "Turma não encontrada."}