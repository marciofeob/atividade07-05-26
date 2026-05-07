# 🎬 Sistema de Gestão – Rede de Cinemas

**Disciplina:** Engenharia de Software  
**Data:** 07/05/2026  
**Aluno:** Marcio Feo  
**Atividade:** Estudo de Caso – Rede de Cinemas

---

## 📋 Sumário

1. [Requisitos Funcionais e Regras de Negócio](#1-requisitos-funcionais-e-regras-de-negócio)
2. [Diagrama de Casos de Uso](#2-diagrama-de-casos-de-uso)
3. [Diagrama de Classes do Domínio](#3-diagrama-de-classes-do-domínio)
4. [Diagramas de Atividade](#4-diagramas-de-atividade)
5. [Diagramas de Sequência](#5-diagramas-de-sequência)
6. [Arquitetura e Implementação](#6-arquitetura-e-implementação)
7. [Como Executar](#7-como-executar)

---

## 1. Requisitos Funcionais e Regras de Negócio

### 1.1 Requisitos Funcionais

| ID   | Requisito |
|------|-----------|
| RF01 | Cadastrar, editar e consultar cinemas da rede |
| RF02 | Cadastrar, editar e consultar filmes (título, duração, gênero, diretor, elenco) |
| RF03 | Criar sessões vinculando filme, cinema, sala e horário |
| RF04 | Registrar o público diário de cada sessão |
| RF05 | Consultar total de público por sessão |
| RF06 | Consultar total de público por filme |
| RF07 | Consultar total de público por cinema |
| RF08 | Listar filmes em cartaz por cinema |
| RF09 | Consultar elenco, diretor e gênero de um filme |

### 1.2 Regras de Negócio

| ID   | Regra |
|------|-------|
| RN01 | Uma sessão só pode ser criada se não houver conflito de horário na mesma sala e cinema |
| RN02 | O intervalo entre o fim de uma sessão e o início da próxima na mesma sala deve ser de no mínimo 15 minutos |
| RN03 | O público registrado em uma sessão não pode exceder a capacidade do cinema |
| RN04 | A duração de uma sessão é calculada automaticamente com base na duração do filme |
| RN05 | Um filme deve estar cadastrado antes de ser vinculado a uma sessão |
| RN06 | Um cinema deve estar cadastrado antes de receber sessões |

---

## 2. Diagrama de Casos de Uso

```mermaid
graph TD
    Admin([👤 Administrador / Funcionário])
    Espect([👤 Espectador])

    UC01[Cadastrar Cinema]
    UC02[Cadastrar Filme]
    UC03[Gerenciar Sessões]
    UC04[Registrar Público]
    UC05[Consultar Relatório de Público]
    UC06[Consultar Filmes em Cartaz]
    UC07[Consultar Detalhes do Filme]

    Admin --> UC01
    Admin --> UC02
    Admin --> UC03
    Admin --> UC04
    Admin --> UC05
    Admin --> UC06
    Espect --> UC06
    Espect --> UC07
```

---

## 3. Diagrama de Classes do Domínio

```mermaid
classDiagram
    class Cinema {
        +int id
        +string nome
        +string cidade
        +string estado
        +string endereco
        +int capacidade
    }

    class Filme {
        +int id
        +string titulo
        +int duracao_min
        +string genero
        +string diretor
        +string elenco
    }

    class Sessao {
        +int id
        +datetime data_hora
        +string sala
        +int intervalo_min
    }

    class RegistroPublico {
        +int id
        +date data
        +int quantidade_publico
    }

    Cinema "1" --> "0..*" Sessao : realiza
    Filme  "1" --> "0..*" Sessao : é exibido em
    Sessao "1" --> "0..*" RegistroPublico : possui
```

---

## 4. Diagramas de Atividade

### 4.1 Criar Sessão

```mermaid
flowchart TD
    A([Início]) --> B[Selecionar Cinema]
    B --> C[Selecionar Filme]
    C --> D[Informar Sala, Data e Hora]
    D --> E{Sala disponível\nno horário?}
    E -- Não --> F[Exibir erro de conflito]
    F --> D
    E -- Sim --> G{Intervalo mínimo\nde 15 min respeitado?}
    G -- Não --> H[Exibir erro de intervalo]
    H --> D
    G -- Sim --> I[Salvar Sessão]
    I --> J([Fim])
```

### 4.2 Registrar Público

```mermaid
flowchart TD
    A([Início]) --> B[Selecionar Sessão]
    B --> C[Informar Quantidade de Público]
    C --> D{Quantidade ≤\nCapacidade do Cinema?}
    D -- Não --> E[Exibir erro de capacidade]
    E --> C
    D -- Sim --> F[Salvar Registro de Público]
    F --> G([Fim])
```

---

## 5. Diagramas de Sequência

### 5.1 Criar Sessão

```mermaid
sequenceDiagram
    actor Admin
    participant View as CLI View
    participant Controller as SessaoController
    participant Service as SessaoService
    participant Repo as SessaoRepository
    participant DB as SQLite

    Admin->>View: Informar dados da sessão
    View->>Controller: criar_sessao(dados)
    Controller->>Service: criar_sessao(dados)
    Service->>Repo: buscar_sessoes_por_sala(cinema_id, sala)
    Repo->>DB: SELECT * FROM sessoes WHERE ...
    DB-->>Repo: lista de sessões
    Repo-->>Service: sessoes_existentes
    Service->>Service: validar_conflito_horario()
    Service->>Service: validar_intervalo_minimo()
    Service->>Repo: salvar(sessao)
    Repo->>DB: INSERT INTO sessoes ...
    DB-->>Repo: id gerado
    Repo-->>Service: sessao_salva
    Service-->>Controller: sessao_salva
    Controller-->>View: sucesso
    View-->>Admin: "Sessão criada com sucesso"
```

### 5.2 Registrar Público

```mermaid
sequenceDiagram
    actor Admin
    participant View as CLI View
    participant Controller as RegistroController
    participant Service as RegistroService
    participant SessaoRepo as SessaoRepository
    participant RegistroRepo as RegistroRepository
    participant DB as SQLite

    Admin->>View: Informar sessão e quantidade
    View->>Controller: registrar_publico(sessao_id, quantidade)
    Controller->>Service: registrar_publico(sessao_id, quantidade)
    Service->>SessaoRepo: buscar_por_id(sessao_id)
    SessaoRepo->>DB: SELECT * FROM sessoes JOIN cinemas ...
    DB-->>SessaoRepo: sessao + capacidade
    SessaoRepo-->>Service: sessao
    Service->>Service: validar_capacidade(quantidade, capacidade)
    Service->>RegistroRepo: salvar(registro)
    RegistroRepo->>DB: INSERT INTO registros_publico ...
    DB-->>RegistroRepo: id gerado
    RegistroRepo-->>Service: registro_salvo
    Service-->>Controller: registro_salvo
    Controller-->>View: sucesso
    View-->>Admin: "Público registrado com sucesso"
```

---

## 6. Arquitetura e Implementação

### Estrutura de Pastas

```
cinema-network/
├── src/
│   ├── models/              # Entidades do domínio (POPOs)
│   │   ├── cinema.py
│   │   ├── filme.py
│   │   ├── sessao.py
│   │   └── registro_publico.py
│   ├── repositories/        # Acesso ao banco de dados (SQLite)
│   │   ├── base_repository.py
│   │   ├── cinema_repository.py
│   │   ├── filme_repository.py
│   │   ├── sessao_repository.py
│   │   └── registro_publico_repository.py
│   ├── services/            # Regras de negócio
│   │   ├── cinema_service.py
│   │   ├── filme_service.py
│   │   ├── sessao_service.py
│   │   └── registro_publico_service.py
│   ├── controllers/         # Orquestração entre View e Service
│   │   ├── cinema_controller.py
│   │   ├── filme_controller.py
│   │   ├── sessao_controller.py
│   │   └── registro_publico_controller.py
│   ├── views/               # Interface CLI
│   │   └── cli_view.py
│   ├── database/            # Configuração e inicialização do SQLite
│   │   └── db.py
│   └── main.py              # Ponto de entrada
└── README.md
```

### Padrão Arquitetural

```
View → Controller → Service → Repository → SQLite
```

- **View**: interface de usuário (CLI)
- **Controller**: recebe input, chama service, retorna resposta
- **Service**: aplica regras de negócio
- **Repository**: persiste e recupera dados do SQLite

---

## 7. Como Executar

### Pré-requisitos

- Python 3.8+
- SQLite (já incluso no Python)

### Execução

```bash
# Clonar o repositório
git clone https://github.com/marciofeob/Atividade-Aula-Max---07-05-2026.git
cd Atividade-Aula-Max---07-05-2026

# Executar o sistema
python src/main.py
```

O banco de dados `cinema.db` será criado automaticamente na primeira execução.

---

> Projeto desenvolvido para a disciplina de Engenharia de Software – ADS 2026
