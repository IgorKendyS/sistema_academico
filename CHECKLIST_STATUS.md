## ✅ CHECKLIST – Sistema Acadêmico Integrado (Cliente-Servidor em Rede Local) - Status

### ✅ Feito (Done)

* **Arquitetura & Persistência**
  * Banco de dados SQLite inicializado automaticamente (`servidor/database.py`) com chaves estrangeiras ativadas.
  * Dados migrados dos dicionários em memória para SQLite nos módulos de turmas, alunos, aulas e atividades.
  * Usuários padrão criados com senhas hash SHA256 e migração de credenciais legadas em texto puro.
* **Comunicação Cliente-Servidor**
  * Servidor TCP/IP com `threading` e gerenciamento de sessão (timeout de 10 minutos).
  * Cliente CLI persistente (`cliente/main.py`) mantendo a conexão após o login e respeitando permissões por perfil.
* **Módulos de Negócio**
  * CRUD completo de turmas, alunos, aulas e atividades integrado ao servidor.
  * Módulo de relatórios com exportação CSV de alunos e turmas (ordenadas por nome).
  * Integração Python ↔ C com QuickSort e nova busca binária utilizada em `alunos.buscar_aluno`.
* **Segurança**
  * Controle de acesso centralizado em `servidor/auth.py`.
  * Senhas armazenadas com hash e validação via `usuarios.autenticar_usuario`.
* **Documentação**
  * `docs/manual_tecnico.md` e `docs/manual_usuario.md` preenchidos com orientações de instalação, uso e arquitetura.
* **Testes Automatizados**
  * Suíte `pytest` com cobertura para módulos de alunos, turmas, relatórios, ordenação (C) e usuários.
  * Execução local finalizada com sucesso (`python -m pytest`).

### ⏳ A Fazer (To Do)

* **Validações Adicionais**
  * Testes de rede multi-cliente em ambiente LAN.
  * Testes de integração Python ↔ C comparando desempenho.
  * Testes de estresse com grande volume de dados.
* **Documentação Complementar**
  * Diagrama de rede atualizado.
  * Roteiro de demonstração (apresentação prática).
