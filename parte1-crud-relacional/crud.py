"""
CRUD (Create, Read, Update, Delete) para as tabelas do esquema "universidade":
usuario, estudante, curso, vinculo

Estrutura das tabelas e dados de exemplo baseados no dump fornecido pelo
professor em aula.
Uso: python crud.py   (executa uma demonstração no final do arquivo)
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

# DEMONSTRAÇÃO
# Dados de exemplo inspirados no dump do professor: nomes de cientistas
# da computação famosos, e os mesmos cursos que aparecem no dump.

if __name__ == "__main__":
    # 1. Cria vários usuários/estudantes
    pessoas = [
        # cpf,           nome,                data_nascimento, email,                          login,        senha,  mat_estudante, mc,  ano_ingresso
        ("22222222301", "Steve Jobs",          "1990-03-05", ["steve@email.com"],              "steve2",     "s1",   "E201", 7.0, 2021),
        ("22222222302", "Alan Turing",         "1912-07-23", ["turing@email.com"],             "alan2",      "s2",   "E202", 9.5, 2021),
        ("22222222303", "Ada Lovelace",        "1985-11-27", ["ada@email.com"],                "ada2",       "s3",   "E203", 8.7, 2022),
        ("22222222304", "Grace Hopper",        "1996-12-10", ["grace@email.com"],              "grace2",     "s4",   "E204", 7.7, 2022),
        ("22222222305", "Donald Knuth",        "1938-01-10", ["knuth@email.com"],              "knuth2",     "s5",   "E205", 6.9, 2023),
    ]

    ids_estudantes = []
    for cpf, nome, nascimento, email, login, senha, mat, mc, ano in pessoas:
        criar_usuario(cpf, nome, nascimento, email=email, login=login, senha=senha)
        criar_estudante(mat, cpf, mc=mc, ano_ingresso=ano)
        ids_estudantes.append(mat)

    print("Usuários/estudantes criados:")
    for usuario in buscar_usuario():
        print(" ", usuario)

    # 2. Cria os mesmos cursos que aparecem no dump do professor
    cursos = [
        ("Ciência da Computação", "Bacharelado", "Vespertino", "São Cristóvão", "Graduação"),
        ("Sistemas de Informação", "Bacharelado", "Noturno", "São Cristóvão", "Graduação"),
        ("Engenharia de Computação", "Bacharelado", "Vespertino", "São Cristóvão", "Graduação"),
    ]
    ids_cursos = [criar_curso(*c) for c in cursos]

    print("\nCursos criados:")
    for curso in buscar_curso():
        print(" ", curso)

    # 3. Cria um vínculo para cada estudante, em cursos diferentes
    ids_vinculos = []
    for i, mat in enumerate(ids_estudantes):
        id_curso = ids_cursos[i % len(ids_cursos)]
        id_v = criar_vinculo(mat, id_curso, status="Ativo", data_entrada="2024-03-01")
        ids_vinculos.append(id_v)

    print("\nVínculos criados:")
    for vinculo in buscar_vinculo():
        print(" ", vinculo)

    # 4. Atualiza o vínculo do primeiro estudante (Steve Jobs) para "Formando"
    atualizar_vinculo(ids_vinculos[0], status="Formando")
    print("\nVínculo atualizado:", buscar_vinculo(ids_vinculos[0]))

    # 5. Deleta o último vínculo criado (Donald Knuth) -- descomente para testar
    # deletar_vinculo(ids_vinculos[-1])