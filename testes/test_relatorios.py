import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from servidor.modulos import relatorios


def test_gerar_relatorio_alunos_csv():
    alunos = [
        {"id": 2, "nome": "Ana", "matricula": "202"},
        {"id": 1, "nome": "Bruno", "matricula": "101"},
    ]

    csv_data = relatorios.gerar_relatorio_alunos_csv(alunos)

    linhas = csv_data.strip().splitlines()
    assert linhas[0] == "ID,Nome,Matrícula"
    assert "2,Ana,202" in linhas
    assert "1,Bruno,101" in linhas


def test_gerar_relatorio_turmas_csv():
    turmas = [
        {"id": 2, "nome": "Turma B", "professor": "Prof. B"},
        {"id": 1, "nome": "Turma A", "professor": "Prof. A"},
    ]

    csv_data = relatorios.gerar_relatorio_turmas_csv(turmas)

    linhas = csv_data.strip().splitlines()
    assert linhas[0] == "ID,Nome,Professor"
    # Deve vir ordenado por nome
    assert linhas[1] == "1,Turma A,Prof. A"
    assert linhas[2] == "2,Turma B,Prof. B"
