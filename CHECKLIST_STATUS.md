## ✅ CHECKLIST – Sistema Acadêmico Integrado (Cliente-Servidor em Rede Local) - Status

### ✅ Feito (Done):

*   **Estrutura do Projeto:**
    *   Criação da estrutura de diretórios (`servidor`, `cliente`, `c_module`, `testes`, `docs`).
    *   Criação de arquivos iniciais (`.gitignore`, `requirements.txt`, `main.py` para cliente/servidor, módulos vazios).
*   **Comunicação Cliente-Servidor:**
    *   Servidor TCP/IP básico com `threading` para múltiplas conexões.
    *   Cliente básico para testar a conexão.
    *   Implementação de comunicação via JSON entre cliente e servidor.
*   **Módulo de Usuários:**
    *   `servidor/modulos/usuarios.py` criado com `USUARIOS` (dummy) e `autenticar_usuario`.
    *   Integração do login no `servidor/main.py`.
    *   Testes de login (sucesso e falha).
*   **Módulo de Turmas:**
    *   `servidor/modulos/turmas.py` criado com `TURMAS` (em memória).
    *   Funções `criar_turma`, `listar_turmas`, `buscar_turma`, `atualizar_turma`, `remover_turma`.
    *   Integração do CRUD de turmas no `servidor/main.py`.
    *   Testes de CRUD de turmas (criação, atualização, listagem, remoção).
*   **Módulo de Alunos:**
    *   `servidor/modulos/alunos.py` criado com `ALUNOS` (em memória).
    *   Funções `criar_aluno`, `listar_aluno`, `buscar_aluno`, `atualizar_aluno`, `remover_aluno`.
    *   Integração do CRUD de alunos no `servidor/main.py`.
    *   Testes de CRUD de alunos (criação, atualização, listagem, remoção).
*   **Módulo de Aulas:**
    *   `servidor/modulos/aulas.py` criado com `AULAS` (em memória).
    *   Funções `registrar_aula`, `listar_aulas_turma`.
    *   Integração das funções de aula no `servidor/main.py`.
    *   Testes de registro e listagem de aulas.
*   **Módulo de Atividades:**
    *   `servidor/modulos/atividades.py` criado com `ATIVIDADES` (em memória).
    *   Funções `enviar_atividade`, `listar_atividades_turma`, `baixar_atividade`.
    *   Integração das funções de atividade no `servidor/main.py`.
    *   Testes de envio, listagem e download de atividades.
*   **Integração Python-C (Ordenação):**
    *   `c_module/modulos.c` criado com implementação de Quick Sort.
    *   Compilação do C para `c_module/modulos.so`.
    *   `servidor/modulos/ordenacao.py` criado com `ctypes` para interface com C.
    *   Integração da ordenação em C na função `listar_turmas`.
*   **Testar de onde parou:**
    *   Verificado se a ordenação está funcionando. O problema era que `proximo_id_turma` não estava sendo resetado entre os testes. A solução foi adicionar uma chamada para resetar os dados no início dos testes.

### ⏳ A Fazer (To Do):

*   **Módulo de Relatórios:**
    *   Criação do módulo de relatórios.
    *   Geração de relatório de alunos em CSV.
    *   Geração de relatório de turmas em CSV, ordenado por nome.
*   **Persistência de Dados:**
    *   Substituído listas em memória por um banco de dados SQLite.
    *   Refatorados os módulos de turmas, alunos, usuários, aulas e atividades para usar o banco de dados.
*   **Segurança:**
    *   Implementado controle de acesso por tipo de usuário (administrador, professor, aluno) para todas as ações.
    *   Implementado gerenciamento de sessões com timeout.
*   **Interface do Cliente:**
    *   Desenvolvida uma interface de linha de comando (CLI) interativa.
*   **Testes:**
    *   Testes unitários mais abrangentes (`unittest` ou `pytest`).
    *   Testes de rede (simulação com dois PCs ou VMs).
    *   Testes de integração Python-C (comparar tempo de execução).
    *   Testes de estresse (grande volume de dados).
*   **Documentação:**
    *   Manual Técnico (descrição dos módulos, diagramas, fluxos).
    *   Manual do Usuário (explicação simples de uso).
    *   Diagrama de Rede.
    *   Demonstração.
*   **Outros Módulos C:**
    *   Implementar busca binária em C para vetor de alunos.
