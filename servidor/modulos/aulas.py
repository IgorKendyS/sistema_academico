from .. import database

def registrar_aula(dados_aula):
    """
    Registra uma nova aula no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO aulas (id_turma, data, topico) VALUES (?, ?, ?)", 
                   (dados_aula.get("id_turma"), dados_aula.get("data"), dados_aula.get("topico")))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    
    nova_aula = {
        "id": novo_id,
        "id_turma": dados_aula.get("id_turma"),
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