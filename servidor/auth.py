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
    "registrar_aula": ["administrador", "professor"],
    "listar_aulas_turma": ["administrador", "professor", "aluno"],
    "remover_aula": ["administrador", "professor"],
    "enviar_atividade": ["administrador", "professor"],
    "listar_atividades_turma": ["administrador", "professor", "aluno"],
    "remover_atividade": ["administrador", "professor"],
    "baixar_atividade": ["administrador", "professor", "aluno"],
    "criar_usuario": ["administrador"],
    "listar_usuarios": ["administrador"],
    "remover_usuario": ["administrador"],
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
