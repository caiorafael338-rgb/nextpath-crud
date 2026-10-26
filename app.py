import os
import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(page_title="NextPath - Carreiras", page_icon="🧭")

def conectar():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "nextpath"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )

def executar(sql, params=None, fetch=False):
    with conectar() as con:
        with con.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None

def listar_areas():
    return executar("SELECT id, nome FROM area ORDER BY nome;", fetch=True)

# ---------- Login ----------
def tela_login():
    st.title("🧭 NextPath")
    st.subheader("Login")
    login = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        try:
            r = executar(
                "SELECT id FROM usuario WHERE login = %s AND senha_hash = crypt(%s, senha_hash);",
                (login, senha), fetch=True)
        except Exception as e:
            st.error(f"Erro ao conectar ao banco: {e}")
            return
        if r:
            st.session_state["logado"] = login
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# ---------- Sistema ----------
def tela_principal():
    st.title("🧭 NextPath - Carreiras")
    st.caption(f"Logado como {st.session_state['logado']}")
    if st.sidebar.button("Sair"):
        del st.session_state["logado"]
        st.rerun()

    areas = listar_areas()
    nomes = {nome: id_ for id_, nome in areas}
    abas = st.tabs(["Consultar", "Cadastrar", "Atualizar", "Excluir", "Áreas", "Resumo"])

    with abas[0]:
        c1, c2 = st.columns(2)
        area = c1.selectbox("Área", ["Todas"] + list(nomes))
        texto = c2.text_input("Título contém")
        smin, smax = st.slider("Faixa salarial (R$)", 0, 20000, (0, 20000), step=500)
        area_id = None if area == "Todas" else nomes[area]
        rows = executar(
            """SELECT c.id, c.titulo, c.descricao, c.salario_medio, a.nome AS area
               FROM carreira c INNER JOIN area a ON a.id = c.area_id
               WHERE (%s::int IS NULL OR c.area_id = %s::int)
                 AND c.titulo ILIKE '%%' || %s || '%%'
                 AND c.salario_medio BETWEEN %s AND %s
               ORDER BY c.titulo;""",
            (area_id, area_id, texto, smin, smax), fetch=True)
        st.dataframe(pd.DataFrame(rows, columns=["id", "título", "descrição", "salário médio", "área"]),
                     use_container_width=True, hide_index=True)

    with abas[1]:
        with st.form("novo"):
            t = st.text_input("Título")
            d = st.text_area("Descrição")
            s = st.number_input("Salário médio", min_value=0.0, step=100.0)
            a = st.selectbox("Área", list(nomes), key="a_novo")
            if st.form_submit_button("Cadastrar"):
                if not t.strip():
                    st.error("Informe o título.")
                else:
                    executar("INSERT INTO carreira (titulo, descricao, salario_medio, area_id) VALUES (%s,%s,%s,%s);",
                             (t.strip(), d, s, nomes[a]))
                    st.success("Carreira cadastrada.")

    carreiras = executar("SELECT id, titulo, descricao, salario_medio, area_id FROM carreira ORDER BY titulo;", fetch=True)

    with abas[2]:
        if not carreiras:
            st.info("Nenhuma carreira cadastrada.")
        else:
            op = st.selectbox("Carreira", carreiras, format_func=lambda r: f"{r[0]} - {r[1]}", key="sel_up")
            ids = [n for n in nomes.values()]
            idx = ids.index(op[4]) if op[4] in ids else 0
            with st.form(f"up{op[0]}"):
                t = st.text_input("Título", op[1])
                d = st.text_area("Descrição", op[2] or "")
                s = st.number_input("Salário médio", min_value=0.0, step=100.0, value=float(op[3] or 0))
                a = st.selectbox("Área", list(nomes), index=idx)
                if st.form_submit_button("Salvar"):
                    executar("UPDATE carreira SET titulo=%s, descricao=%s, salario_medio=%s, area_id=%s WHERE id=%s;",
                             (t.strip(), d, s, nomes[a], op[0]))
                    st.success("Carreira atualizada. Recarregue a aba Consultar.")

    with abas[3]:
        if carreiras:
            op = st.selectbox("Carreira", carreiras, format_func=lambda r: f"{r[0]} - {r[1]}", key="sel_del")
            if st.button("Excluir"):
                executar("DELETE FROM carreira WHERE id = %s;", (op[0],))
                st.success("Carreira excluída.")
                st.rerun()

    with abas[4]:
        nova = st.text_input("Nova área")
        if st.button("Adicionar área") and nova.strip():
            try:
                executar("INSERT INTO area (nome) VALUES (%s);", (nova.strip(),))
                st.rerun()
            except Exception:
                st.error("Área já existe.")

    with abas[5]:
        r = executar("""SELECT a.nome, COUNT(c.id), COALESCE(AVG(c.salario_medio),0)
                        FROM area a LEFT JOIN carreira c ON c.area_id = a.id
                        GROUP BY a.nome ORDER BY a.nome;""", fetch=True)
        st.dataframe(pd.DataFrame(r, columns=["área", "carreiras", "salário médio"]),
                     use_container_width=True, hide_index=True)

if "logado" in st.session_state:
    tela_principal()
else:
    tela_login()
