# Clínica Bem-Estar

Aplicação desktop para gerenciamento de usuários, triagem e filas de atendimento, com interface feita em CustomTkinter e armazenamento local em SQLite.

## Funcionalidades

- Login com acesso direcionado conforme o cargo do usuário.
- Administração para cadastrar e excluir usuários.
- Triagem de pacientes por especialidade e nível de prioridade.
- Geração de senhas e chamada do próximo paciente da fila.
- Painel separado para exibir as chamadas.
- Persistência de usuários, filas e chamadas em banco SQLite.

## Requisitos

- Windows.
- Python 3 e `pip` para executar o código-fonte.
- Tkinter disponível na instalação do Python.

## Executar pelo código-fonte

No PowerShell, abra a pasta do projeto e instale o CustomTkinter:

```powershell
python -m pip install customtkinter
```

Inicie a aplicação:

```powershell
python main.py
```

## Primeiro acesso

Quando não há usuários cadastrados nem um arquivo `usuarios.json` para importação, o banco de dados é inicializado com:

- **Usuário:** `admin`
- **Senha:** `1234`

## Gerar o executável

Instale o PyInstaller:

```powershell
python -m pip install pyinstaller
```

Na pasta do projeto, gere o executável incluindo os arquivos de tema do CustomTkinter:

```powershell
python -m PyInstaller --noconfirm --clean --windowed --name ClinicaBemEstar --collect-all customtkinter main.py
```

O resultado ficará em `dist\ClinicaBemEstar\ClinicaBemEstar.exe`. Mantenha a pasta `ClinicaBemEstar` inteira: o executável usa os arquivos da pasta `_internal`. O banco de dados é criado junto aos arquivos internos do aplicativo; deixe a pasta em um local com permissão de gravação para preservar os dados.

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
