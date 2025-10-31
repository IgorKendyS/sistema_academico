import socket
import json

HOST = "127.0.0.1"
PORT = 9998

def send_request(request):
    """
    Envia uma requisição para o servidor e retorna a resposta.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.send(json.dumps(request).encode('utf-8'))
        response_data = client.recv(1024).decode('utf-8')
        return json.loads(response_data)

def main_menu():
    """
    Exibe o menu principal e lida com a entrada do usuário.
    """
    while True:
        print("\n--- Sistema Acadêmico ---")
        print("1. Login")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            login()
        elif opcao == "2":
            break
        else:
            print("Opção inválida.")

def login():
    """
    Lida com o login do usuário.
    """
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    response = send_request({"acao": "login", "usuario": usuario, "senha": senha})

    if response.get("status") == "ok":
        print(f"Login bem-sucedido! Perfil: {response.get('perfil')}")
        perfil = response.get("perfil")
        if perfil == "administrador":
            menu_administrador()
        elif perfil == "professor":
            menu_professor()
        elif perfil == "aluno":
            menu_aluno()
    else:
        print(f"Erro no login: {response.get('message')}")

if __name__ == "__main__":
    main_menu()

def menu_administrador():
    """
    Exibe o menu do administrador.
    """
    while True:
        print("\n--- Menu do Administrador ---")
        print("1. Criar Turma")
        print("2. Listar Turmas")
        print("3. Remover Turma")
        print("4. Resetar Banco de Dados")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_turma()
        elif opcao == "2":
            listar_turmas()
        elif opcao == "3":
            remover_turma()
        elif opcao == "4":
            resetar_banco_de_dados()
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

def menu_professor():
    """
    Exibe o menu do professor.
    """
    while True:
        print("\n--- Menu do Professor ---")
        print("1. Listar Alunos")
        print("2. Criar Aluno")
        print("3. Registrar Aula")
        print("4. Listar Aulas de uma Turma")
        print("5. Enviar Atividade")
        print("6. Listar Atividades de uma Turma")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_alunos()
        elif opcao == "2":
            criar_aluno()
        elif opcao == "3":
            registrar_aula()
        elif opcao == "4":
            listar_aulas_turma()
        elif opcao == "5":
            enviar_atividade()
        elif opcao == "6":
            listar_atividades_turma()
        elif opcao == "7":
            break
        else:
            print("Opção inválida.")

def menu_aluno():
    """
    Exibe o menu do aluno.
    """
    while True:
        print("\n--- Menu do Aluno ---")
        print("1. Listar Turmas")
        print("2. Listar Aulas de uma Turma")
        print("3. Listar Atividades de uma Turma")
        print("4. Baixar Atividade")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_turmas()
        elif opcao == "2":
            listar_aulas_turma()
        elif opcao == "3":
            listar_atividades_turma()
        elif opcao == "4":
            baixar_atividade()
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

def criar_turma():
    """
    Coleta os dados e envia a requisição para criar uma turma.
    """
    nome = input("Nome da turma: ")
    professor = input("Professor da turma: ")
    response = send_request({"acao": "criar_turma", "dados": {"nome": nome, "professor": professor}})
    if response.get("status") == "ok":
        print("Turma criada com sucesso!")
    else:
        print(f"Erro ao criar turma: {response.get('message')}")

def listar_turmas():
    """
    Envia a requisição para listar as turmas e as exibe.
    """
    response = send_request({"acao": "listar_turmas"})
    if response.get("status") == "ok":
        turmas = response.get("turmas", [])
        if not turmas:
            print("Nenhuma turma cadastrada.")
        else:
            for turma in turmas:
                print(f"ID: {turma['id']}, Nome: {turma['nome']}, Professor: {turma['professor']}")
    else:
        print(f"Erro ao listar turmas: {response.get('message')}")

def remover_turma():
    """
    Coleta o ID da turma e envia a requisição para removê-la.
    """
    id_turma = input("ID da turma a ser removida: ")
    response = send_request({"acao": "remover_turma", "id": int(id_turma)})
    if response.get("status") == "ok":
        print("Turma removida com sucesso!")
    else:
        print(f"Erro ao remover turma: {response.get('message')}")

def resetar_banco_de_dados():
    """
    Envia a requisição para resetar o banco de dados.
    """
    confirmacao = input("Tem certeza que deseja resetar o banco de dados? (s/n): ")
    if confirmacao.lower() == 's':
        response = send_request({"acao": "reset_database"})
        if response.get("status") == "ok":
            print("Banco de dados resetado com sucesso!")
        else:
            print(f"Erro ao resetar o banco de dados: {response.get('message')}")

def listar_alunos():
    """
    Envia a requisição para listar os alunos e os exibe.
    """
    response = send_request({"acao": "listar_alunos"})
    if response.get("status") == "ok":
        alunos = response.get("alunos", [])
        if not alunos:
            print("Nenhum aluno cadastrado.")
        else:
            for aluno in alunos:
                print(f"ID: {aluno['id']}, Nome: {aluno['nome']}, Matrícula: {aluno['matricula']}")
    else:
        print(f"Erro ao listar alunos: {response.get('message')}")

def criar_aluno():
    """
    Coleta os dados e envia a requisição para criar um aluno.
    """
    nome = input("Nome do aluno: ")
    matricula = input("Matrícula do aluno: ")
    response = send_request({"acao": "criar_aluno", "dados": {"nome": nome, "matricula": matricula}})
    if response.get("status") == "ok":
        print("Aluno criado com sucesso!")
    else:
        print(f"Erro ao criar aluno: {response.get('message')}")

def registrar_aula():
    """
    Coleta os dados e envia a requisição para registrar uma aula.
    """
    id_turma = input("ID da turma: ")
    data = input("Data da aula (YYYY-MM-DD): ")
    topico = input("Tópico da aula: ")
    response = send_request({"acao": "registrar_aula", "dados": {"id_turma": int(id_turma), "data": data, "topico": topico}})
    if response.get("status") == "ok":
        print("Aula registrada com sucesso!")
    else:
        print(f"Erro ao registrar aula: {response.get('message')}")

def listar_aulas_turma():
    """
    Coleta o ID da turma e envia a requisição para listar as aulas.
    """
    id_turma = input("ID da turma: ")
    response = send_request({"acao": "listar_aulas_turma", "id_turma": int(id_turma)})
    if response.get("status") == "ok":
        aulas = response.get("aulas", [])
        if not aulas:
            print("Nenhuma aula registrada para esta turma.")
        else:
            for aula in aulas:
                print(f"ID: {aula['id']}, Data: {aula['data']}, Tópico: {aula['topico']}")
    else:
        print(f"Erro ao listar aulas: {response.get('message')}")

def enviar_atividade():
    """
    Coleta os dados e envia a requisição para enviar uma atividade.
    """
    id_turma = input("ID da turma: ")
    titulo = input("Título da atividade: ")
    descricao = input("Descrição da atividade: ")
    response = send_request({"acao": "enviar_atividade", "dados": {"id_turma": int(id_turma), "titulo": titulo, "descricao": descricao}})
    if response.get("status") == "ok":
        print("Atividade enviada com sucesso!")
    else:
        print(f"Erro ao enviar atividade: {response.get('message')}")

def listar_atividades_turma():
    """
    Coleta o ID da turma e envia a requisição para listar as atividades.
    """
    id_turma = input("ID da turma: ")
    response = send_request({"acao": "listar_atividades_turma", "id_turma": int(id_turma)})
    if response.get("status") == "ok":
        atividades = response.get("atividades", [])
        if not atividades:
            print("Nenhuma atividade registrada para esta turma.")
        else:
            for atividade in atividades:
                print(f"ID: {atividade['id']}, Título: {atividade['titulo']}, Descrição: {atividade['descricao']}")
    else:
        print(f"Erro ao listar atividades: {response.get('message')}")

def baixar_atividade():
    """
    Coleta o ID da atividade e envia a requisição para baixá-la.
    """
    id_atividade = input("ID da atividade: ")
    response = send_request({"acao": "baixar_atividade", "id_atividade": int(id_atividade)})
    if response.get("status") == "ok":
        arquivo = response.get("arquivo")
        if arquivo:
            # O arquivo é recebido como uma lista de bytes, então precisamos converter para string
            conteudo = bytes(arquivo).decode('utf-8')
            print(f"Conteúdo da atividade:\n{conteudo}")
        else:
            print("Atividade não tem arquivo.")
    else:
        print(f"Erro ao baixar atividade: {response.get('message')}")