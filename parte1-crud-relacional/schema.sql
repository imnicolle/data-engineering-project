-- Esquema Relacional: usuario, estudante, curso, vinculo
-- Trabalho Prático de Engenharia de Dados
-- Estrutura das tabelas baseada no esquema "universidade" trabalhado em aula
-- (dump fornecido pelo professor André Britto de Carvalho)

DROP SCHEMA IF EXISTS universidade CASCADE;
CREATE SCHEMA universidade;

CREATE DOMAIN universidade.matricula AS VARCHAR(7);
CREATE DOMAIN universidade.tipo_cpf AS NUMERIC(13);

CREATE TYPE universidade.tipo_grau AS ENUM ('Bacharelado', 'Licenciatura Plena');
CREATE TYPE universidade.tipo_nivel AS ENUM ('Graduação', 'Mestrado', 'Doutorado', 'Lato');
CREATE TYPE universidade.tipo_turno AS ENUM ('Matutino', 'Vespertino', 'Noturno', 'Turno Indefinido');
CREATE TYPE universidade.status_estudante AS ENUM ('Ativo', 'Cancelada', 'Formando', 'Graduado');

-- USUARIO

CREATE TABLE universidade.usuario(
    cpf             universidade.tipo_cpf,
    nome            VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    email           VARCHAR[],
    telefone        VARCHAR[],
    login           VARCHAR(45) UNIQUE,
    senha           VARCHAR(32),
    CONSTRAINT pk_usuario PRIMARY KEY (cpf)
);

-- CURSO

CREATE TABLE universidade.curso(
    idCurso SERIAL PRIMARY KEY,
    nome    VARCHAR(100) NOT NULL,
    grau    universidade.tipo_grau,
    turno   universidade.tipo_turno NOT NULL,
    campus  VARCHAR(100),
    nivel   universidade.tipo_nivel,
    CONSTRAINT uq_curso UNIQUE(nome, turno, campus, nivel)
);

-- ESTUDANTE

CREATE TABLE universidade.estudante(
    mat_estudante universidade.matricula,
    cpf           universidade.tipo_cpf,
    MC            DECIMAL(2),
    ano_ingresso  INT,
    CONSTRAINT pk_estudante PRIMARY KEY(mat_estudante),
    CONSTRAINT fk_usuario FOREIGN KEY (cpf) REFERENCES universidade.usuario(cpf)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT uq_cpf UNIQUE(cpf)
);

-- VINCULO

CREATE TABLE universidade.vinculo(
    idVinculo      SERIAL PRIMARY KEY,
    mat_estudante  universidade.matricula,
    curso          INT,
    data_entrada   DATE,
    status         universidade.status_estudante,
    data_saida     DATE,
    CONSTRAINT fk_curso FOREIGN KEY (curso) REFERENCES universidade.curso(idCurso)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_estudante FOREIGN KEY (mat_estudante) REFERENCES universidade.estudante(mat_estudante)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Índices auxiliares
CREATE INDEX idx_vinculo_estudante ON universidade.vinculo(mat_estudante);
CREATE INDEX idx_vinculo_curso ON universidade.vinculo(curso);
