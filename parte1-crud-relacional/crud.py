"""
CRUD (Create, Read, Update, Delete) para as tabelas:
usuario, estudante, curso, vinculo

Uso: python crud.py   (executa uma demonstração no final do arquivo)
"""
from db import get_connection

# USUARIO

def criar_usuario(nome, cpf, email, senha, data_nascimento):
    sql = """
        INSERT INTO usuario (nome, cpf, email, senha, data_nascimento)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_usuario;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, cpf, email, senha, data_nascimento))
            novo_id = cur.fetchone()["id_usuario"]
            conn.commit()
            return novo_id


def buscar_usuario(id_usuario=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if id_usuario:
                cur.execute("SELECT * FROM usuario WHERE id_usuario = %s;", (id_usuario,))
                return cur.fetchone()
            cur.execute("SELECT * FROM usuario ORDER BY id_usuario;")
            return cur.fetchall()


def atualizar_usuario(id_usuario, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [id_usuario]
    sql = f"UPDATE usuario SET {colunas} WHERE id_usuario = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0


def deletar_usuario(id_usuario):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuario WHERE id_usuario = %s;", (id_usuario,))
            conn.commit()
            return cur.rowcount > 0

# CURSO

def criar_curso(codigo, nome, grau, departamento):
    sql = """
        INSERT INTO curso (codigo, nome, grau, departamento)
        VALUES (%s, %s, %s, %s)
        RETURNING id_curso;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (codigo, nome, grau, departamento))
            novo_id = cur.fetchone()["id_curso"]
            conn.commit()
            return novo_id


def buscar_curso(id_curso=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if id_curso:
                cur.execute("SELECT * FROM curso WHERE id_curso = %s;", (id_curso,))
                return cur.fetchone()
            cur.execute("SELECT * FROM curso ORDER BY id_curso;")
            return cur.fetchall()


def atualizar_curso(id_curso, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [id_curso]
    sql = f"UPDATE curso SET {colunas} WHERE id_curso = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0

def deletar_curso(id_curso):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM curso WHERE id_curso = %s;", (id_curso,))
            conn.commit()
            return cur.rowcount > 0

# ESTUDANTE (especialização de usuario)

def criar_estudante(id_estudante, matricula, data_ingresso):
    """id_estudante deve ser um id_usuario já existente na tabela usuario."""
    sql = """
        INSERT INTO estudante (id_estudante, matricula, data_ingresso)
        VALUES (%s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_estudante, matricula, data_ingresso))
            conn.commit()
            return id_estudante


def buscar_estudante(id_estudante=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if id_estudante:
                cur.execute("""
                    SELECT e.*, u.nome, u.cpf, u.email
                    FROM estudante e JOIN usuario u ON u.id_usuario = e.id_estudante
                    WHERE e.id_estudante = %s;
                """, (id_estudante,))
                return cur.fetchone()
            cur.execute("""
                SELECT e.*, u.nome, u.cpf, u.email
                FROM estudante e JOIN usuario u ON u.id_usuario = e.id_estudante
                ORDER BY e.id_estudante;
            """)
            return cur.fetchall()


def atualizar_estudante(id_estudante, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [id_estudante]
    sql = f"UPDATE estudante SET {colunas} WHERE id_estudante = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0


def deletar_estudante(id_estudante):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM estudante WHERE id_estudante = %s;", (id_estudante,))
            conn.commit()
            return cur.rowcount > 0

# VINCULO (liga estudante a curso)

def criar_vinculo(id_estudante, id_curso, status, data_inicio, tipo_ingresso, data_fim=None):
    sql = """
        INSERT INTO vinculo (id_estudante, id_curso, status, data_inicio, data_fim, tipo_ingresso)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id_vinculo;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_estudante, id_curso, status, data_inicio, data_fim, tipo_ingresso))
            novo_id = cur.fetchone()["id_vinculo"]
            conn.commit()
            return novo_id


def buscar_vinculo(id_vinculo=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if id_vinculo:
                cur.execute("SELECT * FROM vinculo WHERE id_vinculo = %s;", (id_vinculo,))
                return cur.fetchone()
            cur.execute("SELECT * FROM vinculo ORDER BY id_vinculo;")
            return cur.fetchall()


def atualizar_vinculo(id_vinculo, **campos):
    if not campos:
        return False
    colunas = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [id_vinculo]
    sql = f"UPDATE vinculo SET {colunas} WHERE id_vinculo = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
            conn.commit()
            return cur.rowcount > 0


def deletar_vinculo(id_vinculo):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vinculo WHERE id_vinculo = %s;", (id_vinculo,))
            conn.commit()
            return cur.rowcount > 0

# DEMONSTRAÇÃO

if __name__ == "__main__":
    # 1. Cria um usuário
    id_u = criar_usuario("Maria Silva", "12345678901", "maria@ufs.br", "senha123", "2003-05-14")
    print("Usuário criado:", buscar_usuario(id_u))

    # 2. Cria um curso
    id_c = criar_curso("CC-01", "Ciência da Computação", "Bacharelado", "DComp")
    print("Curso criado:", buscar_curso(id_c))

    # 3. Transforma o usuário em estudante
    criar_estudante(id_u, "202412345", "2024-03-01")
    print("Estudante criado:", buscar_estudante(id_u))

    # 4. Cria o vínculo entre estudante e curso
    id_v = criar_vinculo(id_u, id_c, "ativo", "2024-03-01", "sisu")
    print("Vínculo criado:", buscar_vinculo(id_v))

    # 5. Atualiza o vínculo
    atualizar_vinculo(id_v, status="trancado")
    print("Vínculo atualizado:", buscar_vinculo(id_v))

    # 6. Deleta o vínculo (não remove estudante nem curso)
    # deletar_vinculo(id_v)
