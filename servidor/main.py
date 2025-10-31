import socket
import threading
import json
import time
from .modulos.usuarios import autenticar_usuario
from .modulos import turmas
from .modulos.alunos import (
    criar_aluno, listar_alunos, atualizar_aluno, remover_aluno
)
from .modulos.aulas import (
    registrar_aula, listar_aulas_turma
)
from .modulos.atividades import (
    enviar_atividade, listar_atividades_turma, baixar_atividade
)
from .modulos import relatorios
from . import database
from . import auth

import time

TIMEOUT = 600 # 10 minutos

def handle_client(client_socket, addr):
    """
    Função para lidar com a conexão de um cliente.
    """
    print(f"[NOVA CONEXÃO] {addr} conectado.", flush=True)
    session = {"perfil": None, "last_activity": time.time()} # Inicializa a sessão

    try:
        while True:
            if time.time() - session["last_activity"] > TIMEOUT:
                print(f"[TIMEOUT] {addr} desconectado por inatividade.", flush=True)
                break

            data = client_socket.recv(1024)
            if not data:
                break
            
            session["last_activity"] = time.time() # Atualiza a atividade
            
            message = json.loads(data.decode('utf-8'))
            print(f"[{addr}] Mensagem JSON recebida: {message}", flush=True)

            response = handle_request(message, session)
            client_socket.send(json.dumps(response).encode('utf-8'))
    
    except ConnectionResetError:
        print(f"[CONEXÃO PERDIDA] Conexão com {addr} foi perdida.", flush=True)
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro com {addr}: {e}", flush=True)
    
    finally:
        print(f"[FIM DA CONEXÃO] {addr} desconectado.", flush=True)
        client_socket.close()

def handle_request(request, session):
    """
    Processa a requisição do cliente e retorna uma resposta.
    """
    acao = request.get("acao")
    perfil = session.get("perfil")

    if acao == "login":
        return login(request, session)

    if not perfil:
        return {"status": "erro", "message": "Usuário não autenticado."}

    if perfil not in auth.PERMISSOES.get(acao, []):
        return {"status": "erro", "message": "Permissão negada."}

    # Ações de Turmas
    if acao == "criar_turma":
        return turmas.criar_turma(request.get("dados"))
    elif acao == "listar_turmas":
        return turmas.listar_turmas(request.get("ordenar_por_id", False))
    elif acao == "atualizar_turma":
        return turmas.atualizar_turma(request.get("id"), request.get("dados"))
    elif acao == "remover_turma":
        return turmas.remover_turma(request.get("id"))
    # Ações de Alunos
    elif acao == "criar_aluno":
        return criar_aluno(request.get("dados"))
    elif acao == "listar_alunos":
        return listar_alunos()
    elif acao == "atualizar_aluno":
        return atualizar_aluno(request.get("id"), request.get("dados"))
    elif acao == "remover_aluno":
        return remover_aluno(request.get("id"))
    # Ações de Aulas
    elif acao == "registrar_aula":
        return registrar_aula(request.get("dados"))
    elif acao == "listar_aulas_turma":
        return listar_aulas_turma(request.get("id_turma"))
    # Ações de Atividades
    elif acao == "enviar_atividade":
        return enviar_atividade(request.get("dados"))
    elif acao == "listar_atividades_turma":
        return listar_atividades_turma(request.get("id_turma"))
    elif acao == "baixar_atividade":
        return baixar_atividade(request.get("id_atividade"))
    elif acao == "reset_database":
        return reset_database()
    # Ações de Relatórios
    elif acao == "gerar_relatorio_alunos":
        lista_alunos = listar_alunos()["alunos"]
        csv_data = relatorios.gerar_relatorio_alunos_csv(lista_alunos)
        return {"status": "ok", "relatorio": csv_data}
    elif acao == "gerar_relatorio_turmas":
        lista_turmas = turmas.listar_turmas()["turmas"]
        csv_data = relatorios.gerar_relatorio_turmas_csv(lista_turmas)
        return {"status": "ok", "relatorio": csv_data}
    else:
        return {"status": "erro", "message": "Ação desconhecida"}

def login(request, session):
    """
    Lida com a requisição de login.
    """
    usuario = request.get("usuario")
    senha = request.get("senha")
    
    resultado = autenticar_usuario(usuario, senha)
    
    if resultado["autenticado"]:
        session["perfil"] = resultado["perfil"]
        return {"status": "ok", "message": "Login bem-sucedido", "perfil": resultado["perfil"]}
    else:
        return {"status": "erro", "message": "Usuário ou senha inválidos"}

def reset_database():
    """
    Limpa todos os dados das tabelas do banco de dados.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM turmas")
    cursor.execute("DELETE FROM alunos")
    cursor.execute("DELETE FROM aulas")
    cursor.execute("DELETE FROM atividades")
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Banco de dados resetado com sucesso."}

def main():
    """
    Função principal para iniciar o servidor.
    """
    database.init_db() # Inicializa o banco de dados
    host = "0.0.0.0"  # Escuta em todas as interfaces de rede
    port = 9998

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Servidor escutando em {host}:{port}", flush=True)

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}", flush=True)

if __name__ == "__main__":
    main()
