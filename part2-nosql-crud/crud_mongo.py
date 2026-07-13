"""
CRUD (Create, Read, Update, Delete) para as entidades:
usuario, estudante, curso, vinculo -- mapeadas em duas coleções MongoDB,
com estrutura baseada no esquema "universidade" trabalhado em aula.

- "usuarios": documentos de usuário (chave: cpf), com subdocumento embutido
  "estudante" (relação 1:1) contendo a lista embutida "vinculos" (relação 1:N).
- "cursos": coleção própria, referenciada pelo campo id_curso dentro de
  cada vínculo (relação N:1).

Uso: python crud_mongo.py   (executa uma demonstração no final do arquivo)
"""
from datetime import datetime
from bson import ObjectId
from mongo_db import get_db

db = get_db()


def _to_datetime(d):
    if d is None or isinstance(d, datetime):
        return d
    return datetime.combine(d, datetime.min.time())

# USUARIO (chave natural: cpf)

def criar_usuario(cpf, nome, data_nascimento=None, email=None, telefone=None, login=None, senha=None):
    """email e telefone devem ser listas de strings, ou None."""
    doc = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": _to_datetime(data_nascimento),
        "email": email,
        "telefone": telefone,
        "login": login,
        "senha": senha,
    }
    resultado = db.usuarios.insert_one(doc)
    return resultado.inserted_id


def buscar_usuario(cpf=None):
    if cpf:
        return db.usuarios.find_one({"cpf": cpf})
    return list(db.usuarios.find())


def atualizar_usuario(cpf, **campos):
    if not campos:
        return False
    resultado = db.usuarios.update_one({"cpf": cpf}, {"$set": campos})
    return resultado.modified_count > 0


def deletar_usuario(cpf):
    resultado = db.usuarios.delete_one({"cpf": cpf})
    return resultado.deleted_count > 0

# CURSO

def criar_curso(nome, turno, grau=None, campus=None, nivel=None):
    """grau: 'Bacharelado' ou 'Licenciatura Plena'
       turno: 'Matutino', 'Vespertino', 'Noturno' ou 'Turno Indefinido'
       nivel: 'Graduação', 'Mestrado', 'Doutorado' ou 'Lato'"""
    doc = {"nome": nome, "grau": grau, "turno": turno, "campus": campus, "nivel": nivel}
    resultado = db.cursos.insert_one(doc)
    return resultado.inserted_id


def buscar_curso(id_curso=None):
    if id_curso:
        return db.cursos.find_one({"_id": ObjectId(id_curso)})
    return list(db.cursos.find())


def atualizar_curso(id_curso, **campos):
    if not campos:
        return False
    resultado = db.cursos.update_one({"_id": ObjectId(id_curso)}, {"$set": campos})
    return resultado.modified_count > 0


def deletar_curso(id_curso):
    resultado = db.cursos.delete_one({"_id": ObjectId(id_curso)})
    return resultado.deleted_count > 0

# ESTUDANTE (subdocumento embutido dentro de usuarios, relação 1:1)

def criar_estudante(cpf, mat_estudante, mc=None, ano_ingresso=None):
    """Transforma um usuário existente em estudante."""
    doc = {
        "estudante.mat_estudante": mat_estudante,
        "estudante.mc": mc,
        "estudante.ano_ingresso": ano_ingresso,
        "estudante.vinculos": [],
    }
    resultado = db.usuarios.update_one({"cpf": cpf}, {"$set": doc})
    return resultado.modified_count > 0


def buscar_estudante(cpf=None):
    filtro = {"estudante": {"$ne": None}}
    if cpf:
        filtro["cpf"] = cpf
        return db.usuarios.find_one(filtro)
    return list(db.usuarios.find(filtro))


def atualizar_estudante(cpf, **campos):
    """campos deve usar as chaves mat_estudante / mc / ano_ingresso."""
    if not campos:
        return False
    updates = {f"estudante.{k}": v for k, v in campos.items()}
    resultado = db.usuarios.update_one({"cpf": cpf}, {"$set": updates})
    return resultado.modified_count > 0


def deletar_estudante(cpf):
    """Remove o vínculo de 'ser estudante', mantendo o usuário base."""
    resultado = db.usuarios.update_one({"cpf": cpf}, {"$unset": {"estudante": ""}})
    return resultado.modified_count > 0

# VINCULO (item dentro da lista embutida usuarios.estudante.vinculos)

def criar_vinculo(cpf, id_curso, status, data_entrada=None, data_saida=None):
    """status: 'Ativo', 'Cancelada', 'Formando' ou 'Graduado'"""
    if not db.cursos.find_one({"_id": ObjectId(id_curso)}):
        raise ValueError(f"Curso {id_curso} não existe.")

    id_vinculo = ObjectId()
    vinculo = {
        "id_vinculo": id_vinculo,
        "id_curso": ObjectId(id_curso),
        "status": status,
        "data_entrada": _to_datetime(data_entrada),
        "data_saida": _to_datetime(data_saida),
    }
    db.usuarios.update_one({"cpf": cpf}, {"$push": {"estudante.vinculos": vinculo}})
    return id_vinculo


def buscar_vinculo(cpf, id_vinculo=None):
    usuario = db.usuarios.find_one({"cpf": cpf})
    if not usuario or not usuario.get("estudante"):
        return None
    vinculos = usuario["estudante"].get("vinculos", [])
    if id_vinculo:
        return next((v for v in vinculos if v["id_vinculo"] == ObjectId(id_vinculo)), None)
    return vinculos


def atualizar_vinculo(cpf, id_vinculo, **campos):
    if not campos:
        return False
    updates = {f"estudante.vinculos.$.{k}": v for k, v in campos.items()}
    resultado = db.usuarios.update_one(
        {"cpf": cpf, "estudante.vinculos.id_vinculo": ObjectId(id_vinculo)},
        {"$set": updates},
    )
    return resultado.modified_count > 0


def deletar_vinculo(cpf, id_vinculo):
    resultado = db.usuarios.update_one(
        {"cpf": cpf},
        {"$pull": {"estudante.vinculos": {"id_vinculo": ObjectId(id_vinculo)}}},
    )
    return resultado.modified_count > 0

# DEMONSTRAÇÃO
# Mesmos dados de exemplo usados na Parte 1 (nomes do dump do professor)

if __name__ == "__main__":
    from datetime import date

    pessoas = [
        ("22222222301", "Steve Jobs", date(1990, 3, 5), ["steve@email.com"], "steve2", "s1", "E201", 7.0, 2021),
        ("22222222302", "Alan Turing", date(1912, 7, 23), ["turing@email.com"], "alan2", "s2", "E202", 9.5, 2021),
        ("22222222303", "Ada Lovelace", date(1985, 11, 27), ["ada@email.com"], "ada2", "s3", "E203", 8.7, 2022),
    ]

    for cpf, nome, nascimento, email, login, senha, mat, mc, ano in pessoas:
        criar_usuario(cpf, nome, nascimento, email=email, login=login, senha=senha)
        criar_estudante(cpf, mat, mc=mc, ano_ingresso=ano)

    print("Usuários/estudantes criados:")
    for u in buscar_usuario():
        print(" ", u)

    id_curso = criar_curso(
        nome="Ciência da Computação", turno="Vespertino",
        grau="Bacharelado", campus="São Cristóvão", nivel="Graduação",
    )
    print("\nCurso criado:", buscar_curso(id_curso))

    cpf_steve = pessoas[0][0]
    id_v = criar_vinculo(cpf_steve, id_curso, status="Ativo", data_entrada=date(2024, 3, 1))
    print("\nVínculo criado:", buscar_vinculo(cpf_steve, id_v))

    atualizar_vinculo(cpf_steve, id_v, status="Formando")
    print("Vínculo atualizado:", buscar_vinculo(cpf_steve, id_v))

    # deletar_vinculo(cpf_steve, id_v)