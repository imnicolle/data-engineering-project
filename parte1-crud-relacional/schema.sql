-- Esquema Relacional: usuario, estudante, curso, vinculo
-- Trabalho Prático de Engenharia de Dados

DROP TABLE IF EXISTS vinculo CASCADE;
DROP TABLE IF EXISTS estudante CASCADE;
DROP TABLE IF EXISTS curso CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;

CREATE TABLE usuario (
    id_usuario      SERIAL PRIMARY KEY,
    nome            VARCHAR(150) NOT NULL,
    cpf             CHAR(11) NOT NULL UNIQUE,
    email           VARCHAR(150) NOT NULL UNIQUE,
    senha           VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL
);

CREATE TABLE curso (
    id_curso    SERIAL PRIMARY KEY,
    codigo      VARCHAR(20) NOT NULL UNIQUE,
    nome        VARCHAR(150) NOT NULL,
    grau        VARCHAR(30) NOT NULL CHECK (grau IN ('Bacharelado', 'Licenciatura', 'Tecnologo')),
    departamento VARCHAR(100) NOT NULL
);

CREATE TABLE estudante (
    id_estudante    INTEGER PRIMARY KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    matricula       VARCHAR(20) NOT NULL UNIQUE,
    data_ingresso   DATE NOT NULL
);

CREATE TABLE vinculo (
    id_vinculo      SERIAL PRIMARY KEY,
    id_estudante    INTEGER NOT NULL REFERENCES estudante(id_estudante) ON DELETE CASCADE,
    id_curso        INTEGER NOT NULL REFERENCES curso(id_curso) ON DELETE CASCADE,
    status          VARCHAR(20) NOT NULL CHECK (status IN ('ativo', 'trancado', 'formado', 'cancelado', 'transferido')),
    data_inicio     DATE NOT NULL,
    data_fim        DATE,
    tipo_ingresso   VARCHAR(30) NOT NULL CHECK (tipo_ingresso IN ('vestibular', 'sisu', 'transferencia', 'reopcao', 'outro')),
    UNIQUE (id_estudante, id_curso, data_inicio)
);

-- Índices auxiliares
CREATE INDEX idx_vinculo_estudante ON vinculo(id_estudante);
CREATE INDEX idx_vinculo_curso ON vinculo(id_curso);
