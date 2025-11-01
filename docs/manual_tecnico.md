## Manual Técnico – Sistema Acadêmico Integrado

### Visão Geral
O sistema é composto por um servidor Python que expõe funcionalidades acadêmicas através de sockets TCP e por um cliente em linha de comando que mantém uma sessão persistente para interagir com essas funcionalidades. Um módulo em C fornece operações de ordenação e busca binária para suporte às consultas.

### Estrutura do Projeto
- `servidor/`: código-fonte do servidor
  - `main.py`: loop principal de atendimento de conexões
  - `database.py`: inicialização e acesso ao SQLite com senhas hash SHA256
  - `auth.py`: mapa de permissões utilizado no roteamento das ações
  - `modulos/`: cada domínio funcional (alunos, turmas, aulas, atividades e relatórios)
- `cliente/main.py`: interface CLI persistente por perfil (administrador, professor e aluno)
  - Navegação suporta retorno com opção `0` e cancelamento em prompts via Enter/`voltar`
- `c_module/modulos.c`: biblioteca compartilhada com QuickSort e busca binária expostos via `ctypes`
- `testes/`: suíte `pytest` com testes unitários e de integração

### Banco de Dados
O SQLite é armazenado em `sistema_academico.db` na raiz do projeto. O módulo `servidor/database.py`:
1. Cria as tabelas (`turmas`, `alunos`, `aulas`, `atividades` e `usuarios`);
2. Garante `PRAGMA foreign_keys = ON`;
3. Insere usuários padrão com senhas hash SHA256 (admin/prof/aluno) e migra registros legados em texto puro.

### Integração Python ↔ C
O arquivo `c_module/modulos.c` implementa QuickSort e busca binária. Para recompilar:

```bash
gcc -shared -o c_module/modulos.so c_module/modulos.c -fPIC
```

O wrapper `servidor/modulos/ordenacao.py` carrega a biblioteca usando `ctypes` e expõe:
- `sort_int_array(lista_de_ints)`: ordenação em C;
- `binary_search(lista_ordenada, alvo)`: índice ou -1 quando não encontrado.

O módulo `alunos` utiliza essas funções para validar a existência de IDs antes de consultar o banco.

### Comunicação Cliente-Servidor
As mensagens são JSON com a chave `acao` e `dados` contextuais. O servidor mantém sessão por conexão (perfil do usuário e timeout). O cliente agora preserva o socket após o login garantindo o respeito às permissões.

### Scripts, Build e Execução
1. (Opcional) Recompile o módulo C conforme bloco anterior.
2. Inicie o servidor:
   ```bash
   python -m servidor.main
   ```
3. Em outro terminal, execute o cliente:
   ```bash
   python -m cliente.main
   ```

### Testes Automatizados
Utilize `pytest` na raiz do projeto:
```bash
pytest
```

A suíte cobre módulos de alunos, turmas, autenticação e geração de relatórios; inclua novos testes seguindo o padrão dentro de `testes/`.
