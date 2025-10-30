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

### ⏳ A Fazer (To Do):

*   **Testar de onde parou:**
    *   Verificar se a ordenação está funcionando, pois tinha erro "Sorting's broken. proximo_id_turma isn't resetting. I'll import the turmas module in main.py and reset the variables there.".
*   **Módulo de Relatórios:**
    *   Geração de relatórios com algoritmos de busca e ordenação (Python pode gerar arquivos `.csv` ou `.pdf`).
*   **Persistência de Dados:**
    *   Substituir listas em memória por um banco de dados (SQLite ou MySQL).
*   **Segurança:**
    *   Implementar controle de acesso por tipo de usuário (administrador, professor, aluno) para todas as ações.
    *   Gerenciamento de sessões (timeout, encerramento limpo).
*   **Interface do Cliente:**
    *   Desenvolver uma interface mais robusta (CLI interativa ou GUI com Tkinter/PyQt).
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
