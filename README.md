# Trabalho Prático de Engenharia de Dados

Repositório do trabalho prático da disciplina de Engenharia de Dados, ministrada pelo professor André Britto de Carvalho (UFS).

O projeto é dividido em três partes: CRUD relacional (PostgreSQL), CRUD NoSQL (MongoDB) e integração de dados em um esquema estrela (ETL com Apache Hop).

## Autoras

- Evilyn Aquino dos Santos
- Nicolle Rillary Santana Silva

## Estrutura do repositório

```
ed-2026/
├── parte1-crud-relacional/    # CRUD em PostgreSQL (AWS RDS)
├── parte2-crud-nosql/         # CRUD em MongoDB (AWS EC2)
└── README.md
```

## Modelo de dados

O projeto trabalha com quatro entidades, presentes tanto na Parte 1 quanto na Parte 2:

- **usuário** — dados pessoais e de acesso (nome, CPF, e-mail, senha, data de nascimento)
- **estudante** — especialização de usuário (matrícula, data de ingresso)
- **curso** — código, nome, grau e departamento
- **vínculo** — associação entre um estudante e um curso ao longo do tempo (status, datas, tipo de ingresso)

---

## Parte 1 — CRUD Relacional (PostgreSQL)

CRUD completo em Python, conectado a uma instância PostgreSQL hospedada no AWS RDS.

### Arquivos
| Arquivo | Descrição |
|---|---|
| `schema.sql` | Script de criação das 4 tabelas e restrições de integridade |
| `db.py` | Módulo de conexão com o banco (lê credenciais do `.env`) |
| `crud.py` | Funções de criação, leitura, atualização e remoção para cada tabela |
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
3. Execute o `schema.sql` no banco (via pgAdmin 4 ou `psql`).
4. Rode a demonstração:
   ```bash
   python crud.py
   ```

---

## Parte 2 — CRUD NoSQL (MongoDB)

CRUD completo em Python, conectado a uma instância própria do MongoDB hospedada em um servidor AWS EC2.

### Mapeamento relacional → MongoDB
- **usuário + estudante** → coleção `usuarios`, com o estudante embutido como subdocumento (relação 1:1)
- **vínculo** → lista embutida dentro do subdocumento `estudante` (relação 1:N)
- **curso** → coleção própria `cursos`, referenciada pelo `ObjectId` dentro de cada vínculo (relação N:1)

### Arquivos
| Arquivo | Descrição |
|---|---|
| `mongo_schema.js` | Script de criação das coleções, validação de esquema (`$jsonSchema`) e índices |
| `mongo_db.py` | Módulo de conexão com o banco (lê credenciais do `.env`) |
| `crud_mongo.py` | Funções de criação, leitura, atualização e remoção para cada entidade |
| `requirements_mongo.txt` | Dependências Python |
| `.env.example` | Modelo das variáveis de ambiente (sem dados reais) |

### Como rodar

1. Crie um arquivo `.env` dentro de `parte2-crud-nosql/` com:
   ```
   MONGO_URI=mongodb://usuario:senha@seu-host:27017/?authSource=admin
   MONGO_DB_NAME=bancoufs_nosql
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements_mongo.txt
   ```
3. Execute o `mongo_schema.js` no MongoDB (via `mongosh` ou pelo shell do MongoDB Compass).
4. Rode a demonstração:
   ```bash
   python crud_mongo.py
   ```

---

## Parte 3 — Integração de Dados (em andamento)

Construção de um esquema estrela e pipelines de ETL com Apache Hop, integrando os dados do banco relacional (Parte 1) com arquivos CSV do portal [dados.ufs.br](https://dados.ufs.br/group/ensino).

*Seção a ser adicionada após a conclusão desta etapa.*

---

## Segurança

Nenhum arquivo `.env` (contendo credenciais reais) é versionado neste repositório — cada pasta possui um `.gitignore` que impede seu envio. Utilize os arquivos `.env.example` como referência para criar sua própria cópia local.
