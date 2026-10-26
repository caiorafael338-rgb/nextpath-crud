# NextPath – Sistema de Carreiras (CRUD com PostgreSQL)

Sistema com interface gráfica (Streamlit) para cadastrar e consultar carreiras por área, inspirado no projeto NextPath (orientação de carreira para jovens).

## Funcionalidades
- Login de usuário (senha protegida com `crypt` do pgcrypto)
- CRUD de carreiras (cadastrar, consultar, atualizar, excluir)
- Duas tabelas relacionadas por chave estrangeira: `carreira.area_id → area.id`
- Filtros em SQL: área, texto no título e faixa salarial
- Resumo com JOIN, COUNT e AVG por área

## Tecnologias
Python 3.10+, Streamlit, psycopg2, pandas, PostgreSQL.

## Configuração do banco
```bash
createdb -U postgres nextpath
psql -U postgres -d nextpath -f sql/schema.sql
psql -U postgres -d nextpath -f sql/seed.sql
```
Variáveis de ambiente (opcionais, padrão entre parênteses): `PGHOST` (localhost), `PGPORT` (5432), `PGDATABASE` (nextpath), `PGUSER` (postgres), `PGPASSWORD` (postgres).

## Execução
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usuário de teste
Usuário: `admin`  Senha: `admin123`

## Arquivos SQL
- `sql/schema.sql`: criação das tabelas
- `sql/seed.sql`: dados iniciais
- `sql/queries.sql`: comandos usados pelo sistema
