# Documentação do Sistema - Rede de Cinemas

## 1. Visão Geral
Este documento descreve os requisitos, regras de negócio e a arquitetura do sistema de gestão para uma rede de cinemas. O sistema foi desenvolvido utilizando a arquitetura MVC (Model-View-Controller) em camadas (Service, Repository) com persistência em SQLite.

## 2. Levantamento de Requisitos

### 2.1 Requisitos Funcionais (RF)
* **RF01:** O sistema deve permitir o cadastro de novos cinemas (nome, cidade, estado, endereço e capacidade).
* **RF02:** O sistema deve listar todos os cinemas cadastrados.
* **RF03:** O sistema deve permitir o cadastro de filmes (título, duração, gênero, diretor e elenco).
* **RF04:** O sistema deve listar todos os filmes e consultar detalhes específicos de um filme.
* **RF05:** O sistema deve permitir a criação de sessões, vinculando um filme a um cinema em uma data, hora e sala específicas.
* **RF06:** O sistema deve listar as sessões disponíveis (geral ou filtradas por cinema).
* **RF07:** O sistema deve permitir o registro diário da quantidade de público para uma sessão específica.
* **RF08:** O sistema deve gerar relatórios com a totalização de público agrupada por sessão, por filme e por cinema.

### 2.2 Requisitos Não Funcionais (RNF)
* **RNF01:** O sistema deve ser desenvolvido na linguagem Python.
* **RNF02:** Os dados devem ser persistidos localmente utilizando um banco de dados SQLite (`cinema.db`).
* **RNF03:** O projeto deve seguir a arquitetura MVC combinada com os padrões Service e Repository.
* **RNF04:** A interface de interação do usuário deve ser via Linha de Comando (CLI).

## 3. Regras de Negócio (RN)
* **RN01:** A capacidade de público de um cinema deve ser obrigatoriamente maior que zero.
* **RN02:** A duração de um filme deve ser obrigatoriamente maior que zero minutos.
* **RN03:** Toda sessão criada deve prever um intervalo mínimo obrigatório (padrão de 15 minutos) entre exibições.
* **RN04:** A quantidade de público registrada em uma sessão não pode ser negativa.
* **RN05:** (Recomendação) A quantidade de público registrada não deve ultrapassar a capacidade máxima do cinema onde a sessão ocorre.

## 4. Diagramas do Sistema
Os diagramas do projeto foram modelados em PlantUML do JÉBÃO Jeebs e encontram-se na pasta `docs/diagramas`.

1. **Casos de Uso:** `casos_de_uso.puml`
<img width="467" height="474" alt="casosdeuso" src="https://github.com/user-attachments/assets/9dd162d5-6adc-411d-92c7-4b958f379fdc" />

2. **Classes de Domínio:** `classes.puml`
<img width="331" height="489" alt="classes" src="https://github.com/user-attachments/assets/899b2f51-8ffe-46f8-8499-08d0ea052d3c" />

3. **Atividades:** `atividades.puml`
<img width="629" height="531" alt="atividades" src="https://github.com/user-attachments/assets/43750256-42f9-44a1-8bc4-fb99caf8bce6" />

4. **Sequência:** `sequencia.puml`
<img width="1271" height="530" alt="sequencia" src="https://github.com/user-attachments/assets/a5867986-1630-4b14-af6c-6b8ff24de871" />

