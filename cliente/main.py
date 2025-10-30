import socket
import json

def main():
    """
    Função principal para iniciar o cliente e se conectar ao servidor.
    """
    host = "127.0.0.1"  # Conectar ao localhost
    port = 9998

    # Criar Turma C com id 3
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        message = {"acao": "criar_turma", "dados": {"id": 3, "nome": "Turma C", "professor": "Prof. C"}}
        client.send(json.dumps(message).encode('utf-8'))
        response_data = client.recv(1024).decode('utf-8')
        print(f"[SERVIDOR] Resposta JSON recebida: {json.loads(response_data)}")

    # Criar Turma A com id 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        message = {"acao": "criar_turma", "dados": {"id": 1, "nome": "Turma A", "professor": "Prof. A"}}
        client.send(json.dumps(message).encode('utf-8'))
        response_data = client.recv(1024).decode('utf-8')
        print(f"[SERVIDOR] Resposta JSON recebida: {json.loads(response_data)}")

    # Criar Turma B com id 2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        message = {"acao": "criar_turma", "dados": {"id": 2, "nome": "Turma B", "professor": "Prof. B"}}
        client.send(json.dumps(message).encode('utf-8'))
        response_data = client.recv(1024).decode('utf-8')
        print(f"[SERVIDOR] Resposta JSON recebida: {json.loads(response_data)}")

    # Listar turmas com ordenação
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        message = {"acao": "listar_turmas", "ordenar_por_id": True}
        client.send(json.dumps(message).encode('utf-8'))
        print(f"\n[CLIENTE] Mensagem JSON enviada: {message}")
        response_data = client.recv(1024).decode('utf-8')
        response = json.loads(response_data)
        print(f"[SERVIDOR] Resposta JSON recebida: {response}")

if __name__ == "__main__":
    main()
