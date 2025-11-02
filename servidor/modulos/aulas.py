from .. import database

def registrar_aula(dados_aula):
    """
    Registra uma nova aula no banco de dados.
    """
    id_turma = dados_aula.get("id_turma")
    
    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Verificar se a turma existe
    cursor.execute("SELECT COUNT(*) FROM turmas WHERE id = ?", (id_turma,))
    if cursor.fetchone()[0] == 0:
        conn.close()
        return {"status": "erro", "message": "ID da turma inexistente."}

    cursor.execute("INSERT INTO aulas (id_turma, data, topico) VALUES (?, ?, ?)", 
                   (id_turma, dados_aula.get("data"), dados_aula.get("topico")))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    
    nova_aula = {
        "id": novo_id,
        "id_turma": id_turma,
        "data": dados_aula.get("data"),
        "topico": dados_aula.get("topico")
    }
    
    return {"status": "ok", "aula": nova_aula}

def listar_aulas_turma(id_turma):
    """
    Retorna a lista de todas as aulas de uma determinada turma.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aulas WHERE id_turma = ?", (id_turma,))
    aulas_db = cursor.fetchall()
    conn.close()

    aulas = [dict(row) for row in aulas_db]
    return {"status": "ok", "aulas": aulas}

def remover_aula(id_aula):
    """
    Remove uma aula do banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aulas WHERE id = ?", (id_aula,))
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Aula removida com sucesso."}