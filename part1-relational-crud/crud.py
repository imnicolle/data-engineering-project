"""
CRUD (Create, Read, Update, Delete) para as tabelas do esquema "universidade":
usuario, estudante, curso, vinculo

Estrutura das tabelas baseada no dump fornecido pelo professor em aula.
Este módulo contém apenas as funções de manipulação de dados -- para
interagir com elas via terminal, use o menu.py.
"""
from db import get_connection

# USUARIO (chave primária: cpf)

def criar_usuario(cpf, nome, data_nascimento, email=None, telefone=None, login=None, senha=None):
    """email e telefone devem ser listas de strings (ex: ["a@x.com"]), ou None."""
    sql = """
        INSERT INTO universidade.usuario (cpf, nome, data_nascimento, email, telefone, login, senha)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING cpf;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cpf, nome, data_nascimento, email, telefone, login, senha))
            conn.commit()
            return cur.fetchone()["cpf"]


def buscar_usuario(cpf=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if cpf:
                cur.execute("SELECT * FROM universidade.usuario WHERE cpf = %s;", (cpf,))
                return cur.fetchone()
            cur.execute("SELECT * FROM universidade.usuario ORDER BY cpf;")
            return cur.fetchall()


def atualizar_usuario(cpf, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [cpf]
    sql = f"UPDATE universidade.usuario SET {colunas} WHERE cpf = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0


def deletar_usuario(cpf):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM universidade.usuario WHERE cpf = %s;", (cpf,))
            conn.commit()
            return cur.rowcount > 0

# CURSO (chave primária: idcurso, gerada automaticamente)

def criar_curso(nome, grau, turno, campus=None, nivel=None):
    """grau: 'Bacharelado' ou 'Licenciatura Plena'
       turno: 'Matutino', 'Vespertino', 'Noturno' ou 'Turno Indefinido'
       nivel: 'Graduação', 'Mestrado', 'Doutorado' ou 'Lato'"""
    sql = """
        INSERT INTO universidade.curso (nome, grau, turno, campus, nivel)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING idcurso;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, grau, turno, campus, nivel))
            conn.commit()
            return cur.fetchone()["idcurso"]


def buscar_curso(id_curso=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if id_curso:
                cur.execute("SELECT * FROM universidade.curso WHERE idcurso = %s;", (id_curso,))
                return cur.fetchone()
            cur.execute("SELECT * FROM universidade.curso ORDER BY idcurso;")
            return cur.fetchall()


def atualizar_curso(id_curso, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [id_curso]
    sql = f"UPDATE universidade.curso SET {colunas} WHERE idcurso = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0


def deletar_curso(id_curso):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM universidade.curso WHERE idcurso = %s;", (id_curso,))
            conn.commit()
            return cur.rowcount > 0

# ESTUDANTE (chave primária: mat_estudante | referencia usuario por cpf)

def criar_estudante(mat_estudante, cpf, mc=None, ano_ingresso=None):
    """mat_estudante deve ter até 7 caracteres (domínio matricula).
       cpf deve ser de um usuário já existente."""
    sql = """
        INSERT INTO universidade.estudante (mat_estudante, cpf, mc, ano_ingresso)
        VALUES (%s, %s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (mat_estudante, cpf, mc, ano_ingresso))
            conn.commit()
            return mat_estudante


def buscar_estudante(mat_estudante=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if mat_estudante:
                cur.execute("""
                    SELECT e.*, u.nome, u.email, u.data_nascimento
                    FROM universidade.estudante e
                    JOIN universidade.usuario u ON u.cpf = e.cpf
                    WHERE e.mat_estudante = %s;
                """, (mat_estudante,))
                return cur.fetchone()
            cur.execute("""
                SELECT e.*, u.nome, u.email, u.data_nascimento
                FROM universidade.estudante e
                JOIN universidade.usuario u ON u.cpf = e.cpf
                ORDER BY e.mat_estudante;
            """)
            return cur.fetchall()


def atualizar_estudante(mat_estudante, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [mat_estudante]
    sql = f"UPDATE universidade.estudante SET {colunas} WHERE mat_estudante = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0


def deletar_estudante(mat_estudante):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM universidade.estudante WHERE mat_estudante = %s;", (mat_estudante,))
            conn.commit()
            return cur.rowcount > 0

# VINCULO (liga estudante a curso | chave primária: idvinculo)

def criar_vinculo(mat_estudante, curso, status, data_entrada=None, data_saida=None):
    """status: 'Ativo', 'Cancelada', 'Formando' ou 'Graduado'
       curso: idcurso (inteiro)"""
    sql = """
        INSERT INTO universidade.vinculo (mat_estudante, curso, data_entrada, status, data_saida)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING idvinculo;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (mat_estudante, curso, data_entrada, status, data_saida))
            conn.commit()
            return cur.fetchone()["idvinculo"]


def buscar_vinculo(id_vinculo=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if id_vinculo:
                cur.execute("SELECT * FROM universidade.vinculo WHERE idvinculo = %s;", (id_vinculo,))
                return cur.fetchone()
            cur.execute("SELECT * FROM universidade.vinculo ORDER BY idvinculo;")
            return cur.fetchall()


def atualizar_vinculo(id_vinculo, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [id_vinculo]
    sql = f"UPDATE universidade.vinculo SET {colunas} WHERE idvinculo = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0


def deletar_vinculo(id_vinculo):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM universidade.vinculo WHERE idvinculo = %s;", (id_vinculo,))
            conn.commit()
            return cur.rowcount > 0


# ----------------------------------------------------------------------
# Este módulo contém apenas as operações de manipulação de dados (CRUD).
# Ele não imprime nada na tela nem contém dados fixos de exemplo --
# quem cuida da interação com o usuário é o menu.py, e quem cuida da
# formatação/exibição dos resultados é o exibicao.py.
# ----------------------------------------------------------------------
