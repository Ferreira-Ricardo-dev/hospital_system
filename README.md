# 🩺 Clínica Bem-Estar — Sistema de Triagem e Chamada de Pacientes

Aplicação desktop para gerenciamento de usuários, triagem e filas de atendimento, com interface feita em **CustomTkinter**, armazenamento local em **SQLite** e estrutura de dados **Heap Binária (heapq)** para ordenação dinâmica das filas por especialidade.

---

## Funcionalidades

- Login com acesso direcionado conforme o cargo do usuário.
- Administração para cadastrar e excluir usuários.
- Triagem de pacientes por especialidade e nível de prioridade.
- Geração de senhas e chamada do próximo paciente da fila.
- Painel separado para exibir as chamadas.
- Persistência de usuários, filas e chamadas em banco SQLite.

---

## Regras de Negócio da Fila de Prioridade

O motor de filas (`controllers/fila_controller.py`) utiliza uma *min-heap* (`heapq`) estruturada com tuplas no formato `(peso, ordem_chegada, dados_paciente)`, garantindo complexidade $O(\log n)$ e desempate justo por ordem de chegada:

| Prioridade | Peso | Prefixo da Senha | Critério de Aplicação |
| :--- | :---: | :---: | :--- |
| **Emergência** | `1` | `EMG` | Casos urgentes selecionados na triagem |
| **Preferencial** | `2` | `PRF` | Idosos ($\ge 60$ anos, preenchido automaticamente), gestantes e PCD |
| **Normal** | `3` | `NRM` | Demais atendimentos eletivos |

---

## Estrutura do Banco de Dados (`SQLite3`)

O módulo `database.py` cria e gerencia o arquivo `hospital_system.db` com quatro tabelas principais e controle de versão de esquema (`PRAGMA user_version`):

- **`usuarios`**: Armazena credenciais e perfis (`id`, `nome`, `senha`, `cargo`, `data_cadastro`).
- **`fila_espera`**: Persiste os pacientes aguardando atendimento (`id`, `senha`, `nome`, `idade`, `especialidade`, `prioridade`, `peso`, `data_chegada`).
- **`contadores_senha`**: Mantém a numeração sequencial por prefixo (`EMG`, `PRF`, `NRM`).
- **`ultima_chamada`**: Registra a última senha chamada para exibição no painel (`senha`, `nome`, `especialidade`, `prioridade`, `consultorio`, `data_chamada`).

---

## Requisitos

- **Sistema Operacional:** Windows 10 ou 11.
- **Python:** Versão 3.10 ou superior (com `tkinter` e `sqlite3` habilitados na instalação).

---

## Executar pelo código-fonte

### Passo a Passo

1. Clone ou baixe o repositório e abra o terminal (PowerShell) na pasta raiz do projeto.
2. *(Opcional, mas recomendado)* Crie e ative um ambiente virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Instale a dependência gráfica:
   ```powershell
   python -m pip install customtkinter
   ```
4. Execute a aplicação:
   ```powershell
   python main.py
   ```

### Primeiro Acesso
Na primeira inicialização (quando `hospital_system.db` ainda não existe):
- Se houver um arquivo `usuarios.json` válido na pasta raiz, os usuários serão importados automaticamente para o SQLite.
- Caso contrário, o sistema criará automaticamente o administrador padrão:
  - **Usuário:** `admin`
  - **Senha:** `1234`

---

## Estrutura do projeto

```text
hospital_system/
├── main.py
├── database.py
├── controllers/
│   ├── autenticacao.py
│   └── fila_controller.py
└── views/
    ├── admin_view.py
    ├── atendente_view.py
    ├── login_view.py
    └── painel_tv_view.py
```

---

## Executar pelo Executável (Windows 10/11)

Não é necessário ter Python ou dependências instaladas para usar a versão compilada:

1. Copie o arquivo `ClinicaBemEstar.exe` (localizado na pasta `dist/`) para uma pasta com permissão de escrita (ex.: `Área de Trabalho` ou `Documentos`).
2. Dê um duplo clique em `ClinicaBemEstar.exe`.
   - *Nota:* Se o Windows Defender SmartScreen exibir um aviso de aplicativo não reconhecido, clique em **Mais informações** > **Executar assim mesmo**.
3. O arquivo `hospital_system.db` será criado automaticamente ao lado do executável para armazenar os registros.
