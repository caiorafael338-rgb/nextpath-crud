-- Execute conectado ao banco nextpath (veja README)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS usuario (
    id          SERIAL PRIMARY KEY,
    login       VARCHAR(50)  NOT NULL UNIQUE,
    senha_hash  TEXT         NOT NULL
);

CREATE TABLE IF NOT EXISTS area (
    id    SERIAL PRIMARY KEY,
    nome  VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS carreira (
    id             SERIAL PRIMARY KEY,
    titulo         VARCHAR(80)   NOT NULL,
    descricao      TEXT,
    salario_medio  NUMERIC(10,2) CHECK (salario_medio >= 0),
    area_id        INT NOT NULL REFERENCES area(id) ON DELETE RESTRICT
);
