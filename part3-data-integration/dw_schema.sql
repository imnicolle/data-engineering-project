-- Esquema Estrela: turmas de graduação
-- Trabalho Prático de Engenharia de Dados - Parte 3
-- Execute em um banco de dados dedicado, separado do
-- banco relacional da Parte 1, na mesma instância RDS.

DROP TABLE IF EXISTS fato_turma CASCADE;
DROP TABLE IF EXISTS dim_professor CASCADE;
DROP TABLE IF EXISTS dim_disciplina CASCADE;
DROP TABLE IF EXISTS dim_departamento CASCADE;
DROP TABLE IF EXISTS dim_semestre CASCADE;
DROP TABLE IF EXISTS dim_campus CASCADE;

-- DIMENSÃO: Departamento

CREATE TABLE dim_departamento (
    id_departamento     SERIAL PRIMARY KEY,
    sigla               VARCHAR(20) NOT NULL UNIQUE,  -- chave natural
    nome                VARCHAR(150) NOT NULL
);

-- DIMENSÃO: Professor

CREATE TABLE dim_professor (
    id_professor        SERIAL PRIMARY KEY,
    matricula           VARCHAR(30) NOT NULL UNIQUE,  -- chave natural (mat_professor)
    nome                VARCHAR(150) NOT NULL,
    tipo_jornada        VARCHAR(50),                  -- ex: 20h, 40h, DE
    formacao             VARCHAR(100),                 -- ex: Doutorado, Mestrado
    id_departamento_lotacao INTEGER REFERENCES dim_departamento(id_departamento)
);

-- DIMENSÃO: Disciplina (componente curricular)

CREATE TABLE dim_disciplina (
    id_disciplina       SERIAL PRIMARY KEY,
    codigo              VARCHAR(30) NOT NULL UNIQUE,  -- chave natural (cod_disc)
    nome                VARCHAR(150) NOT NULL,
    id_departamento     INTEGER REFERENCES dim_departamento(id_departamento),
    cr_total            INTEGER  -- número de créditos
);

-- DIMENSÃO: Semestre

CREATE TABLE dim_semestre (
    id_semestre         SERIAL PRIMARY KEY,
    ano                 INTEGER NOT NULL,
    periodo             INTEGER NOT NULL CHECK (periodo IN (1, 2)),
    UNIQUE (ano, periodo)  -- chave natural composta
);

-- DIMENSÃO: Campus

CREATE TABLE dim_campus (
    id_campus           SERIAL PRIMARY KEY,
    nome                VARCHAR(100) NOT NULL UNIQUE  -- chave natural
);

-- FATO: Turma
-- Grão: uma linha por turma (professor + disciplina + semestre)

CREATE TABLE fato_turma (
    id_turma                    SERIAL PRIMARY KEY,
    id_professor                INTEGER NOT NULL REFERENCES dim_professor(id_professor),
    id_disciplina                INTEGER NOT NULL REFERENCES dim_disciplina(id_disciplina),
    id_departamento              INTEGER NOT NULL REFERENCES dim_departamento(id_departamento),
    id_semestre                  INTEGER NOT NULL REFERENCES dim_semestre(id_semestre),
    id_campus                   INTEGER REFERENCES dim_campus(id_campus),
    num_discentes_matriculados   INTEGER NOT NULL DEFAULT 0,
    media_notas                 NUMERIC(4,2),   -- pode ser NULL (nem sempre disponível)
    num_aprovados                INTEGER,        -- pode ser NULL
    num_reprovados               INTEGER         -- pode ser NULL
);

CREATE INDEX idx_fato_turma_professor ON fato_turma(id_professor);
CREATE INDEX idx_fato_turma_disciplina ON fato_turma(id_disciplina);
CREATE INDEX idx_fato_turma_semestre ON fato_turma(id_semestre);

-- ------------------------------------------------------------
-- Usuário dedicado para as rotinas de ETL (Apache Hop)
-- Rode como usuário master (postgres) uma única vez, no banco dw_ufs.
-- Descomente e ajuste a senha antes de rodar.
-- ------------------------------------------------------------
-- CREATE USER etl_hop WITH PASSWORD 'DEFINA_UMA_SENHA_AQUI';
-- GRANT CONNECT ON DATABASE dw_ufs TO etl_hop;
-- GRANT USAGE ON SCHEMA public TO etl_hop;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO etl_hop;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO etl_hop;
