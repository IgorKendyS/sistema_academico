import json
import socket
from pathlib import Path
from typing import Optional

HOST = "127.0.0.1"
PORT = 9998
BUFFER_SIZE = 65536
CANCEL_TOKENS = {"", "0", "voltar", "cancelar", "sair"}


class ClientConnection:
    """
    Gerencia a conexão persistente com o servidor para manter a sessão ativa.
    """

    def __init__(self, host=HOST, port=PORT):
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(2)
        self._socket.connect((self._host, self._port))

    def send_request(self, request: dict):
        """
        Envia uma requisição JSON para o servidor e retorna a resposta decodificada.
        """
        payload = json.dumps(request).encode("utf-8")
        self._socket.sendall(payload)

        chunks = []
        while True:
            try:
                chunk = self._socket.recv(BUFFER_SIZE)
            except socket.timeout:
                break

            if not chunk:
                break

            chunks.append(chunk)

            if len(chunk) < BUFFER_SIZE:
                break

        if not chunks:
            raise ConnectionError("Servidor não respondeu.")

        response_bytes = b"".join(chunks)
        return json.loads(response_bytes.decode("utf-8"))

    def close(self):
        if self._socket:
            try:
                self._socket.close()
            finally:
                self._socket = None


def prompt_text(prompt: str, allow_cancel: bool = True) -> Optional[str]:
    """
    Solicita entrada de texto do usuário com suporte a cancelamento.
    """
    valor = input(prompt).strip()
    if allow_cancel and valor.lower() in CANCEL_TOKENS:
        print("Operação cancelada.")
        return None
    return valor


def prompt_int(prompt: str) -> Optional[int]:
    """
    Solicita entrada numérica com suporte a cancelamento e validação.
    """
    while True:
        valor = prompt_text(prompt, allow_cancel=True)
        if valor is None:
            return None
        try:
            return int(valor)
        except ValueError:
            print("Digite um número válido ou pressione Enter para voltar.")


def main_menu():
    """
    Loop principal de interação do cliente.
    """
    while True:
        print("\n--- Sistema Acadêmico ---")
        print("1. Login")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            iniciar_sessao()
        elif opcao == "2":
            print("Encerrando cliente.")
            break
        else:
            print("Opção inválida.")


def iniciar_sessao():
    """
    Realiza o login e, em caso de sucesso, mantém a sessão ativa.
    """
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    try:
        conexao = ClientConnection()
    except OSError as exc:
        print(f"Falha ao conectar ao servidor: {exc}")
        return

    try:
        resposta = conexao.send_request(
            {"acao": "login", "usuario": usuario, "senha": senha}
        )
    except (ConnectionError, json.JSONDecodeError) as exc:
        print(f"Erro ao processar resposta do servidor: {exc}")
        conexao.close()
        return

    if resposta.get("status") != "ok":
        print(f"Erro no login: {resposta.get('message')}")
        conexao.close()
        return

    perfil = resposta.get("perfil")
    print(f"Login bem-sucedido! Perfil: {perfil}")

    try:
        if perfil == "administrador":
            menu_administrador(conexao)
        elif perfil == "professor":
            menu_professor(conexao)
        elif perfil == "aluno":
            menu_aluno(conexao)
        else:
            print("Perfil desconhecido.")
    finally:
        conexao.close()
        print("Sessão encerrada.")


def menu_administrador(conexao: ClientConnection):
    """
    Exibe o menu do administrador.
    """
    while True:
        print("\n--- Menu do Administrador ---")
        print("0. Voltar")
        print("1. Criar Turma")
        print("2. Listar Turmas")
        print("3. Remover Turma")
        print("4. Resetar Banco de Dados")
        print("5. Gerar Relatório de Turmas (CSV)")
        print("6. Gerar Relatório de Alunos (CSV)")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break
        elif opcao == "1":
            criar_turma(conexao)
        elif opcao == "2":
            listar_turmas(conexao)
        elif opcao == "3":
            remover_turma(conexao)
        elif opcao == "4":
            resetar_banco_de_dados(conexao)
        elif opcao == "5":
            gerar_relatorio_turmas(conexao)
        elif opcao == "6":
            gerar_relatorio_alunos(conexao)
        elif opcao == "7":
            break
        else:
            print("Opção inválida.")


def menu_professor(conexao: ClientConnection):
    """
    Exibe o menu do professor.
    """
    while True:
        print("\n--- Menu do Professor ---")
        print("0. Voltar")
        print("1. Listar Alunos")
        print("2. Criar Aluno")
        print("3. Registrar Aula")
        print("4. Listar Aulas de uma Turma")
        print("5. Enviar Atividade")
        print("6. Listar Atividades de uma Turma")
        print("7. Gerar Relatório de Alunos (CSV)")
        print("8. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break
        elif opcao == "1":
            listar_alunos(conexao)
        elif opcao == "2":
            criar_aluno(conexao)
        elif opcao == "3":
            registrar_aula(conexao)
        elif opcao == "4":
            listar_aulas_turma(conexao)
        elif opcao == "5":
            enviar_atividade(conexao)
        elif opcao == "6":
            listar_atividades_turma(conexao)
        elif opcao == "7":
            gerar_relatorio_alunos(conexao)
        elif opcao == "8":
            break
        else:
            print("Opção inválida.")


def menu_aluno(conexao: ClientConnection):
    """
    Exibe o menu do aluno.
    """
    while True:
        print("\n--- Menu do Aluno ---")
        print("0. Voltar")
        print("1. Listar Turmas")
        print("2. Listar Aulas de uma Turma")
        print("3. Listar Atividades de uma Turma")
        print("4. Baixar Atividade")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break
        elif opcao == "1":
            listar_turmas(conexao)
        elif opcao == "2":
            listar_aulas_turma(conexao)
        elif opcao == "3":
            listar_atividades_turma(conexao)
        elif opcao == "4":
            baixar_atividade(conexao)
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")


def criar_turma(conexao: ClientConnection):
    nome = prompt_text("Nome da turma (Enter para voltar): ")
    if nome is None:
        return

    professor = prompt_text("Professor da turma (Enter para voltar): ")
    if professor is None:
        return

    resposta = conexao.send_request(
        {"acao": "criar_turma", "dados": {"nome": nome, "professor": professor}}
    )
    if resposta.get("status") == "ok":
        print("Turma criada com sucesso!")
    else:
        print(f"Erro ao criar turma: {resposta.get('message')}")


def listar_turmas(conexao: ClientConnection):
    resposta = conexao.send_request({"acao": "listar_turmas"})
    if resposta.get("status") == "ok":
        turmas = resposta.get("turmas", [])
        if not turmas:
            print("Nenhuma turma cadastrada.")
        else:
            for turma in turmas:
                print(
                    f"ID: {turma['id']}, Nome: {turma['nome']}, Professor: {turma['professor']}"
                )
    else:
        print(f"Erro ao listar turmas: {resposta.get('message')}")


def remover_turma(conexao: ClientConnection):
    id_turma = prompt_int("ID da turma a ser removida (Enter para voltar): ")
    if id_turma is None:
        return

    resposta = conexao.send_request({"acao": "remover_turma", "id": id_turma})
    if resposta.get("status") == "ok":
        print("Turma removida com sucesso!")
    else:
        print(f"Erro ao remover turma: {resposta.get('message')}")


def resetar_banco_de_dados(conexao: ClientConnection):
    confirmacao = input("Tem certeza que deseja resetar o banco de dados? (s/n): ")
    if confirmacao.lower() == "s":
        resposta = conexao.send_request({"acao": "reset_database"})
        if resposta.get("status") == "ok":
            print("Banco de dados resetado com sucesso!")
        else:
            print(f"Erro ao resetar o banco de dados: {resposta.get('message')}")


def listar_alunos(conexao: ClientConnection):
    resposta = conexao.send_request({"acao": "listar_alunos"})
    if resposta.get("status") == "ok":
        alunos = resposta.get("alunos", [])
        if not alunos:
            print("Nenhum aluno cadastrado.")
        else:
            for aluno in alunos:
                print(
                    f"ID: {aluno['id']}, Nome: {aluno['nome']}, Matrícula: {aluno['matricula']}"
                )
    else:
        print(f"Erro ao listar alunos: {resposta.get('message')}")


def criar_aluno(conexao: ClientConnection):
    nome = prompt_text("Nome do aluno (Enter para voltar): ")
    if nome is None:
        return

    matricula = prompt_text("Matrícula do aluno (Enter para voltar): ")
    if matricula is None:
        return

    resposta = conexao.send_request(
        {"acao": "criar_aluno", "dados": {"nome": nome, "matricula": matricula}}
    )
    if resposta.get("status") == "ok":
        print("Aluno criado com sucesso!")
    else:
        print(f"Erro ao criar aluno: {resposta.get('message')}")


def registrar_aula(conexao: ClientConnection):
    id_turma = prompt_int("ID da turma (Enter para voltar): ")
    if id_turma is None:
        return

    data = prompt_text("Data da aula (YYYY-MM-DD) (Enter para voltar): ")
    if data is None:
        return

    topico = prompt_text("Tópico da aula (Enter para voltar): ")
    if topico is None:
        return

    resposta = conexao.send_request(
        {
            "acao": "registrar_aula",
            "dados": {"id_turma": id_turma, "data": data, "topico": topico},
        }
    )
    if resposta.get("status") == "ok":
        print("Aula registrada com sucesso!")
    else:
        print(f"Erro ao registrar aula: {resposta.get('message')}")


def listar_aulas_turma(conexao: ClientConnection):
    id_turma = prompt_int("ID da turma (Enter para voltar): ")
    if id_turma is None:
        return

    resposta = conexao.send_request({"acao": "listar_aulas_turma", "id_turma": id_turma})
    if resposta.get("status") == "ok":
        aulas = resposta.get("aulas", [])
        if not aulas:
            print("Nenhuma aula registrada para esta turma.")
        else:
            for aula in aulas:
                print(
                    f"ID: {aula['id']}, Data: {aula['data']}, Tópico: {aula['topico']}"
                )
    else:
        print(f"Erro ao listar aulas: {resposta.get('message')}")


def enviar_atividade(conexao: ClientConnection):
    id_turma = prompt_int("ID da turma (Enter para voltar): ")
    if id_turma is None:
        return

    titulo = prompt_text("Título da atividade (Enter para voltar): ")
    if titulo is None:
        return

    descricao = prompt_text("Descrição da atividade (Enter para voltar): ")
    if descricao is None:
        return

    resposta = conexao.send_request(
        {
            "acao": "enviar_atividade",
            "dados": {
                "id_turma": id_turma,
                "titulo": titulo,
                "descricao": descricao,
                "arquivo": None,
            },
        }
    )
    if resposta.get("status") == "ok":
        print("Atividade enviada com sucesso!")
    else:
        print(f"Erro ao enviar atividade: {resposta.get('message')}")


def listar_atividades_turma(conexao: ClientConnection):
    id_turma = prompt_int("ID da turma (Enter para voltar): ")
    if id_turma is None:
        return

    resposta = conexao.send_request({"acao": "listar_atividades_turma", "id_turma": id_turma})
    if resposta.get("status") == "ok":
        atividades = resposta.get("atividades", [])
        if not atividades:
            print("Nenhuma atividade registrada para esta turma.")
        else:
            for atividade in atividades:
                print(
                    f"ID: {atividade['id']}, Título: {atividade['titulo']}, Descrição: {atividade['descricao']}"
                )
    else:
        print(f"Erro ao listar atividades: {resposta.get('message')}")


def baixar_atividade(conexao: ClientConnection):
    id_atividade = prompt_int("ID da atividade (Enter para voltar): ")
    if id_atividade is None:
        return

    resposta = conexao.send_request({"acao": "baixar_atividade", "id_atividade": id_atividade})
    if resposta.get("status") == "ok":
        arquivo = resposta.get("arquivo")
        if arquivo:
            conteudo = bytes(arquivo).decode("utf-8")
            print(f"Conteúdo da atividade:\n{conteudo}")
        else:
            print("Atividade não tem arquivo.")
    else:
        print(f"Erro ao baixar atividade: {resposta.get('message')}")


def gerar_relatorio_turmas(conexao: ClientConnection):
    resposta = conexao.send_request({"acao": "gerar_relatorio_turmas"})
    if resposta.get("status") == "ok":
        _salvar_ou_exibir_relatorio("relatorio_turmas.csv", resposta.get("relatorio"))
    else:
        print(f"Erro ao gerar relatório: {resposta.get('message')}")


def gerar_relatorio_alunos(conexao: ClientConnection):
    resposta = conexao.send_request({"acao": "gerar_relatorio_alunos"})
    if resposta.get("status") == "ok":
        _salvar_ou_exibir_relatorio("relatorio_alunos.csv", resposta.get("relatorio"))
    else:
        print(f"Erro ao gerar relatório: {resposta.get('message')}")


def _salvar_ou_exibir_relatorio(nome_padrao: str, conteudo: Optional[str]):
    """
    Oferece ao usuário a opção de salvar o relatório em disco ou apenas exibi-lo.
    """
    if not conteudo:
        print("Relatório vazio.")
        return

    escolha = input("Deseja salvar o relatório em arquivo? (s/n): ").strip().lower()
    if escolha == "s":
        caminho_informado = input(
            f"Caminho do arquivo (padrão: {nome_padrao} na pasta atual): "
        ).strip()
        caminho = Path(caminho_informado) if caminho_informado else Path(nome_padrao)
        caminho.write_text(conteudo, encoding="utf-8")
        print(f"Relatório salvo em {caminho.resolve()}")
    else:
        print("\n--- Relatório ---")
        print(conteudo)


if __name__ == "__main__":
    main_menu()
