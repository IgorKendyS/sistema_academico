## Manual do Usuário – Cliente CLI

### Pré-requisitos
1. Servidor em execução (`python -m servidor.main`);
2. Cliente executado em outro terminal (`python -m cliente.main`);
3. Credenciais disponíveis:
   - Administrador: `admin / admin`
   - Professor: `prof / prof`
   - Aluno: `aluno / aluno`

### Fluxo de Uso
1. **Login**: informe usuário e senha. O cliente manterá sessão ativa até você escolher “Sair” ou “Voltar” no menu.
2. **Navegação**:
   - Em qualquer menu, escolha `0` para voltar ao nível anterior.
   - Em prompts de formulário (ex.: informar ID, nome ou descrição), pressione Enter ou digite `voltar` para cancelar a operação atual.
3. **Menus por Perfil**:
   - **Administrador**
     - Criar, listar e remover turmas;
     - Resetar o banco (limpa cadastros, preserva usuários);
     - Gerar relatórios CSV de turmas ou alunos (salvar em arquivo ou exibir no terminal).
   - **Professor**
     - Listar/criar alunos;
     - Registrar aulas e listar por turma;
     - Enviar e listar atividades;
     - Gerar relatório CSV de alunos.
   - **Aluno**
     - Listar turmas, aulas e atividades;
     - Baixar o conteúdo de atividades disponíveis.
4. **Relatórios**
   - Ao escolher gerar relatório, decida entre salvar em arquivo (informe caminho ou aceite o padrão) ou apenas visualizar.

### Encerramento
Selecione “Sair” ou “Voltar” no menu atual. A sessão é finalizada automaticamente e a conexão com o servidor encerrada.
