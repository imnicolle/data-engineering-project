# Trabalho Prático de Engenharia de Dados

Repositório do trabalho prático da disciplina de Engenharia de Dados, ministrada pelo professor André Britto de Carvalho (UFS).

O projeto é dividido em três partes: CRUD relacional (PostgreSQL), CRUD NoSQL (MongoDB) e integração de dados em um esquema estrela (ETL com Apache Hop).

## Discentes

- Evilyn Aquino dos Santos 
- Nicolle Rillary Santana Silva

## Estrutura do repositório

```
data-engineering-project/
├── parte1-crud-relacional/    # CRUD em PostgreSQL (AWS RDS)
├── parte2-crud-nosql/         # CRUD em MongoDB (AWS EC2)
├── parte3-integracao-de-dados/ # Esquema estrela + ETL (Apache Hop)
└── README.md
```

## Modelo de dados

A estrutura das tabelas segue o esquema relacional **"universidade"** trabalhado em aula (dump fornecido pelo professor). Esse esquema tem 16 tabelas ao todo; o CRUD desenvolvido neste trabalho (Partes 1 e 2) manipula especificamente quatro delas:

- **usuario** — chave: `cpf`. Dados pessoais e de acesso (nome, data de nascimento, e-mail e telefone em lista, login, senha)
- **estudante** — chave: `mat_estudante`. Especialização de usuário (referencia `usuario` por `cpf`; campos `mc` e `ano_ingresso`)
- **curso** — chave: `idcurso`. Definido por nome, grau (Bacharelado/Licenciatura Plena), turno, campus e nível
- **vinculo** — chave: `idvinculo`. Associação entre um estudante e um curso ao longo do tempo (status: Ativo/Cancelada/Formando/Graduado; datas de entrada e saída)

As demais 12 tabelas do esquema do professor (`professor`, `departamento`, `disciplina`, `semestre`, `turma`, `leciona`, `cursa`, `projeto`, `plano`, `sala`, `horario`, `alocacao`) fazem parte do banco relacional completo e servem de fonte de dados para a Parte 3 (ETL / esquema estrela).

---

## Parte 1 — CRUD Relacional (PostgreSQL)

CRUD completo em Python, conectado a uma instância PostgreSQL hospedada no AWS RDS.

### Arquivos
| Arquivo | Descrição |
|---|---|
| `dump_completo_professor.sql` | Script original do professor: cria o esquema `universidade` completo (16 tabelas) com os dados de exemplo |
| `db.py` | Módulo de conexão com o banco (lê credenciais do `.env`) |
| `crud.py` | Funções puras de criação, leitura, atualização e remoção para usuario/curso/estudante/vinculo (16 funções, sem interface de usuário) |
| `exibicao.py` | Funções responsáveis apenas por formatar e imprimir os dados na tela |
| `menu.py` | Interface de linha de comando (menu interativo) — é o programa que o usuário efetivamente executa |
| `requirements.txt` | Dependências Python |

### Como rodar

1. Crie um arquivo `.env` dentro de `parte1-crud-relacional/` com:
   ```
   DB_HOST=seu-endpoint.rds.amazonaws.com
   DB_PORT=5432
   DB_NAME=nome_do_banco
   DB_USER=postgres
   DB_PASSWORD=sua_senha
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o `dump_completo_professor.sql` no banco (via pgAdmin 4 ou `psql`) — isso cria as 16 tabelas do esquema `universidade`, incluindo as 4 usadas pelo CRUD.
4. Rode o programa interativo:
   ```bash
   python menu.py
   ```
   Isso abre um menu no terminal, onde é possível escolher a entidade (usuário/curso/estudante/vínculo) e a operação (criar/buscar/listar/atualizar/deletar), digitando os dados na hora.

---

## Parte 2 — CRUD NoSQL (MongoDB)

CRUD completo em Python, conectado a uma instância própria do MongoDB hospedada em um servidor AWS EC2.

### Mapeamento relacional → MongoDB

O mapeamento cobre **todas as 16 tabelas** do esquema do professor, representadas em 7 coleções:

| Tabela(s) relacional(is) | Representação no MongoDB |
|---|---|
| `usuario` | Coleção `usuarios` (chave natural: `cpf`) |
| `estudante`, `professor` | Subdocumentos embutidos em `usuarios` (relação 1:1) |
| `vinculo`, `cursa`, `plano` | Listas embutidas dentro de `usuarios.estudante` (relação 1:N) |
| `curso` | Coleção própria `cursos` |
| `departamento` | Coleção própria `departamentos` |
| `disciplina` | Coleção própria `disciplinas` |
| `semestre` | Coleção própria `semestres` |
| `projeto` | Coleção própria `projetos` |
| `turma`, `leciona`, `sala`, `horario`, `alocacao` | Coleção `turmas`, com `professores` e `alocacoes` embutidos |

O **CRUD em código** (`crud_mongo.py`) manipula apenas as quatro entidades pedidas no enunciado (usuário, estudante, curso, vínculo) — as demais coleções existem só para fins de representação/mapeamento, sem operações de CRUD associadas.

### Arquivos
| Arquivo | Descrição |
|---|---|
| `mongo_schema.js` | Script de criação de todas as 7 coleções, com validação de esquema (`$jsonSchema`) e índices |
| `mongo_db.py` | Módulo de conexão com o banco (lê credenciais do `.env`) |
| `crud_mongo.py` | Funções de criação, leitura, atualização e remoção para usuário/estudante/curso/vínculo |
| `requirements_mongo.txt` | Dependências Python |
| `.env.example` | Modelo das variáveis de ambiente (sem dados reais) |

### Como rodar

1. Crie um arquivo `.env` dentro de `parte2-crud-nosql/` com:
   ```
   MONGO_URI=mongodb://usuario:senha@endereco-da-sua-ec2:27017/?authSource=admin
   MONGO_DB_NAME=bancoufs_nosql
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements_mongo.txt
   ```
3. Execute o `mongo_schema.js` no MongoDB (via `mongosh` ou pelo shell do MongoDB Compass) — recomenda-se colar em blocos pequenos (um `db.createCollection(...)` por vez).
4. Rode o script de teste:
   ```bash
   python crud_mongo.py
   ```

---

## Parte 3 — Integração de Dados (em andamento)

Construção de um esquema estrela e pipelines de ETL com Apache Hop, integrando os dados do banco relacional (Parte 1) com arquivos CSV do portal [dados.ufs.br](https://dados.ufs.br/group/ensino).

O esquema estrela modela turmas de graduação, associando professor, disciplina, departamento, semestre e campus, com as métricas de matriculados, média de notas, aprovados e reprovados.

### Arquivos
| Arquivo | Descrição |
|---|---|
| `dw_schema.sql` | Script de criação das tabelas de dimensão e da tabela de fatos |
| `carga_dim_departamento.hpl` | Pipeline de carga da dimensão Departamento |
| `carga_dim_professor.hpl` | Pipeline de carga da dimensão Professor |
| `carga_dim_disciplina.hpl` | Pipeline de carga da dimensão Disciplina |
| `carga_dim_semestre.hpl` | Pipeline de carga da dimensão Semestre |
| `carga_dim_campus.hpl` | Pipeline de carga da dimensão Campus |
| `carga_fato_turma.hpl` | Pipeline de carga da tabela de fatos Turma |
| `uni-csv-unidades-academicas-da-ufs.csv`, `doc-csv-docentes-da-ufs.csv`, `com-csv-componentes-curriculares-da-ufs.csv`, `tur-csv-turmas-de-2025.csv` | Fontes de dados do portal dados.ufs.br |

### Fontes de dados
- **Relacional (Parte 1):** todas as linhas originais do dump, mais as linhas inseridas via CRUD.
- **CSV (dados.ufs.br):** Unidades Acadêmicas, Componentes Curriculares, Docentes e Turmas (2019–2025).

### Como rodar

1. Crie um banco de dados dedicado no mesmo servidor RDS da Parte 1 (separado do banco relacional) e execute `dw_schema.sql`.
2. No Apache Hop, crie uma conexão de banco chamada `dw_ufs` apontando para esse banco.
3. Abra os pipelines dentro de um projeto Hop cuja raiz seja a pasta `parte3-integracao-de-dados/` — os CSVs de entrada são referenciados por caminho relativo (`${Internal.Entry.Current.Directory}`).
4. Execute primeiro os pipelines de dimensão (`carga_dim_*.hpl`) e, por último, `carga_fato_turma.hpl`.

---

## Segurança

Nenhum arquivo `.env` (contendo credenciais reais) é versionado neste repositório — cada pasta possui um `.gitignore` que impede seu envio. Utilize os arquivos `.env.example` como referência para criar sua própria cópia local.
