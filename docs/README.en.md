<<<<<<< HEAD
# Data Engineering Coursework Project

Repository for the practical coursework of the Data Engineering course, taught by professor André Britto de Carvalho (UFS).

The project is divided into three parts: relational CRUD (PostgreSQL), NoSQL CRUD (MongoDB), and data integration into a star schema (ETL with Apache Hop).

## Students

- Evilyn Aquino dos Santos
- Nicolle Rillary Santana Silva

## Repository structure

```
data-engineering-project/
├── part1-relational-crud/      # CRUD in PostgreSQL (AWS RDS)
├── part2-nosql-crud/           # CRUD in MongoDB (AWS EC2)
├── part3-data-integration/     # Star schema + ETL (Apache Hop)
└── README.md
```

## Data model

The table structure follows the **"universidade"** relational schema covered in class (dump provided by the professor). This schema has 16 tables in total; the CRUD built for this coursework (Parts 1 and 2) specifically manipulates four of them:

- **usuario** — key: `cpf`. Personal and access data (name, date of birth, email and phone list, login, password)
- **estudante** — key: `mat_estudante`. User specialization (references `usuario` via `cpf`; fields `mc` and `ano_ingresso`)
- **curso** — key: `idcurso`. Defined by name, degree level (Bacharelado/Licenciatura Plena), shift, campus, and level
- **vinculo** — key: `idvinculo`. Association between a student and a course over time (status: Ativo/Cancelada/Formando/Graduado; start and end dates)

The other 12 tables in the professor's schema (`professor`, `departamento`, `disciplina`, `semestre`, `turma`, `leciona`, `cursa`, `projeto`, `plano`, `sala`, `horario`, `alocacao`) are part of the full relational database and serve as the data source for Part 3 (ETL / star schema).

---

## Part 1 — Relational CRUD (PostgreSQL)

Complete CRUD in Python, connected to a PostgreSQL instance hosted on AWS RDS.

### Files
| File | Description |
|---|---|
| `dump_completo_professor.sql` | Professor's original script: creates the complete `universidade` schema (16 tables) with sample data |
| `db.py` | Database connection module (reads credentials from `.env`) |
| `crud.py` | Pure create, read, update, and delete functions for usuario/curso/estudante/vinculo (16 functions, no user interface) |
| `exibicao.py` | Functions responsible only for formatting and printing data to the screen |
| `menu.py` | Command-line interface (interactive menu) — the program the user actually runs |
| `requirements.txt` | Python dependencies |

### How to run

1. Create a `.env` file inside `part1-relational-crud/` with:
   ```
   DB_HOST=your-endpoint.rds.amazonaws.com
   DB_PORT=5432
   DB_NAME=database_name
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run `dump_completo_professor.sql` against the database (via pgAdmin 4 or `psql`) — this creates all 16 tables of the `universidade` schema, including the 4 used by the CRUD.
4. Run the interactive program:
   ```bash
   python menu.py
   ```
   This opens a terminal menu where you can choose the entity (usuario/curso/estudante/vinculo) and the operation (create/find/list/update/delete), typing the data in on the spot.

---

## Part 2 — NoSQL CRUD (MongoDB)

Complete CRUD in Python, connected to a self-hosted MongoDB instance running on an AWS EC2 server.

### Relational → MongoDB mapping

The mapping covers **all 16 tables** of the professor's schema, represented in 7 collections:

| Relational table(s) | MongoDB representation |
|---|---|
| `usuario` | `usuarios` collection (natural key: `cpf`) |
| `estudante`, `professor` | Subdocuments embedded in `usuarios` (1:1 relationship) |
| `vinculo`, `cursa`, `plano` | Lists embedded inside `usuarios.estudante` (1:N relationship) |
| `curso` | Own `cursos` collection |
| `departamento` | Own `departamentos` collection |
| `disciplina` | Own `disciplinas` collection |
| `semestre` | Own `semestres` collection |
| `projeto` | Own `projetos` collection |
| `turma`, `leciona`, `sala`, `horario`, `alocacao` | `turmas` collection, with `professores` and `alocacoes` embedded |

The **CRUD in code** (`crud_mongo.py`) only manipulates the four entities requested in the assignment (usuario, estudante, curso, vinculo) — the remaining collections exist purely for representation/mapping purposes, with no associated CRUD operations.

### Files
| File | Description |
|---|---|
| `mongo_schema.js` | Script that creates all 7 collections, with schema validation (`$jsonSchema`) and indexes |
| `mongo_db.py` | Database connection module (reads credentials from `.env`) |
| `crud_mongo.py` | Create, read, update, and delete functions for usuario/estudante/curso/vinculo |
| `requirements_mongo.txt` | Python dependencies |
| `.env.example` | Template for environment variables (no real data) |

### How to run

1. Create a `.env` file inside `part2-nosql-crud/` with:
   ```
   MONGO_URI=mongodb://user:password@your-ec2-address:27017/?authSource=admin
   MONGO_DB_NAME=bancoufs_nosql
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements_mongo.txt
   ```
3. Run `mongo_schema.js` against MongoDB (via `mongosh` or the MongoDB Compass shell) — it's recommended to paste it in small chunks (one `db.createCollection(...)` at a time).
4. Run the test script:
   ```bash
   python crud_mongo.py
   ```

---

## Part 3 — Data Integration (in progress)

Building a star schema and ETL pipelines with Apache Hop, integrating data from the relational database (Part 1) with CSV files from the [dados.ufs.br](https://dados.ufs.br/group/ensino) portal.

The star schema models undergraduate class sections, linking professor, course subject, department, semester, and campus, along with metrics for enrolled students, average grade, passed, and failed counts.

### Files
| File | Description |
|---|---|
| `dw_schema.sql` | Script that creates the dimension tables and the fact table |
| `carga_dim_departamento.hpl` | Load pipeline for the Department dimension |
| `carga_dim_professor.hpl` | Load pipeline for the Professor dimension |
| `carga_dim_disciplina.hpl` | Load pipeline for the Course Subject dimension |
| `carga_dim_semestre.hpl` | Load pipeline for the Semester dimension |
| `carga_dim_campus.hpl` | Load pipeline for the Campus dimension |
| `carga_fato_turma.hpl` | Load pipeline for the Class Section fact table |
| `uni-csv-unidades-academicas-da-ufs.csv`, `doc-csv-docentes-da-ufs.csv`, `com-csv-componentes-curriculares-da-ufs.csv`, `tur-csv-turmas-de-2025.csv` | Data sources from the dados.ufs.br portal |

### Data sources
- **Relational (Part 1):** all original rows from the dump, plus rows inserted via CRUD.
- **CSV (dados.ufs.br):** Academic Units, Course Subjects, Faculty, and Class Sections (2019–2025).

### How to run

1. Create a dedicated database on the same RDS server used in Part 1 (separate from the relational database) and run `dw_schema.sql`.
2. In Apache Hop, create a database connection named `dw_ufs` pointing to that database.
3. Open the pipelines inside a Hop project rooted at the `part3-data-integration/` folder — the input CSVs are referenced by relative path (`${Internal.Entry.Current.Directory}`).
4. Run the dimension pipelines first (`carga_dim_*.hpl`), and `carga_fato_turma.hpl` last.

---

## Security

No `.env` file (containing real credentials) is tracked in this repository — each folder has a `.gitignore` that prevents it from being committed. Use the `.env.example` files as a reference to create your own local copy.
=======

>>>>>>> f78693f42e71d11b6e09e82cd71733df71dc3abf
