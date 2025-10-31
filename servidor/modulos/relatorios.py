import csv
import io

def gerar_relatorio_alunos_csv(alunos):
    """
    Gera um relatório de alunos em formato CSV.

    Args:
        alunos (list): Lista de dicionários de alunos.

    Returns:
        str: String com o conteúdo do CSV.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Escreve o cabeçalho
    writer.writerow(["ID", "Nome", "Matrícula"])

    # Escreve os dados dos alunos
    for aluno in alunos:
        writer.writerow([aluno.get("id"), aluno.get("nome"), aluno.get("matricula")])

    return output.getvalue()

def gerar_relatorio_turmas_csv(turmas):
    """
    Gera um relatório de turmas em formato CSV, ordenado por nome.

    Args:
        turmas (list): Lista de dicionários de turmas.

    Returns:
        str: String com o conteúdo do CSV.
    """
    # Ordena as turmas por nome
    turmas_sorted = sorted(turmas, key=lambda x: x['nome'])

    output = io.StringIO()
    writer = csv.writer(output)

    # Escreve o cabeçalho
    writer.writerow(["ID", "Nome", "Professor"])

    # Escreve os dados das turmas
    for turma in turmas_sorted:
        writer.writerow([turma.get("id"), turma.get("nome"), turma.get("professor")])

    return output.getvalue()
