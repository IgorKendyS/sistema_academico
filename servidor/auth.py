from functools import wraps

PERMISSOES = {
    "criar_turma": ["administrador"],
    "listar_turmas": ["administrador", "professor", "aluno"],
    "atualizar_turma": ["administrador", "professor"],
    "remover_turma": ["administrador"],
    "criar_aluno": ["administrador", "professor"],
    "listar_alunos": ["administrador", "professor"],
    "atualizar_aluno": ["administrador", "professor"],
    "remover_aluno": ["administrador", "professor"],
    "registrar_aula": ["professor"],
    "listar_aulas_turma": ["professor", "aluno"],
    "enviar_atividade": ["professor"],
    "listar_atividades_turma": ["professor", "aluno"],
    "baixar_atividade": ["professor", "aluno"],
    "gerar_relatorio_alunos": ["administrador", "professor"],
    "gerar_relatorio_turmas": ["administrador", "professor"],
    "reset_database": ["administrador"],
}

def requer_permissao(acao):
    def decorator(func):
        @wraps(func)
        def wrapper(request, session):
            perfil = session.get("perfil")
            if perfil in PERMISSOES.get(acao, []):
                return func(request, session)
            elif acao == "login": # O login não precisa de permissão
                return func(request, session)
            else:
                return {"status": "erro", "message": "Permissão negada."}
        return wrapper
    return decorator
