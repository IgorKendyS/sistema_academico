from .. import database
from .ordenacao import binary_search, sort_int_array

def criar_aluno(dados_aluno):
    """
    Cria um novo aluno e o insere no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO alunos (nome, matricula) VALUES (?, ?)", 
                       (dados_aluno.get("nome"), dados_aluno.get("matricula")))
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        
        novo_aluno = {
            "id": novo_id,
            "nome": dados_aluno.get("nome"),
            "matricula": dados_aluno.get("matricula")
        }
        
        return {"status": "ok", "aluno": novo_aluno}
    except database.sqlite3.IntegrityError:
        conn.close()
        return {"status": "erro", "message": "Matrícula já existe."}

def listar_alunos():
    """
    Retorna a lista de todos os alunos cadastrados no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos")
    alunos_db = cursor.fetchall()
    conn.close()

    alunos = [dict(row) for row in alunos_db]
    return {"status": "ok", "alunos": alunos}

def buscar_aluno(id_aluno):
    """
    Busca um aluno pelo seu ID no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM alunos")
    ids_db = cursor.fetchall()

    ids = [row["id"] for row in ids_db]
    sorted_ids = sort_int_array(ids) if ids else []

    if binary_search(sorted_ids, id_aluno) == -1:
        conn.close()
        return None

    cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
    aluno_db = cursor.fetchone()
    conn.close()
    
    if aluno_db:
        return dict(aluno_db)
    return None

def atualizar_aluno(id_aluno, dados_aluno):
    """
    Atualiza os dados de um aluno no banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE alunos SET nome = ?, matricula = ? WHERE id = ?", 
                       (dados_aluno.get("nome"), dados_aluno.get("matricula"), id_aluno))
        conn.commit()
        updated_rows = cursor.rowcount
        conn.close()
        
        if updated_rows > 0:
            return {"status": "ok", "message": "Aluno atualizado com sucesso."}
        else:
            return {"status": "erro", "message": "Aluno não encontrado."}
    except database.sqlite3.IntegrityError:
        conn.close()
        return {"status": "erro", "message": "Matrícula já existe."}

def remover_aluno(id_aluno):
    """
    Remove um aluno do banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    
    if deleted_rows > 0:
        return {"status": "ok", "message": "Aluno removido com sucesso."}
    else:
        return {"status": "erro", "message": "Aluno não encontrado."}
