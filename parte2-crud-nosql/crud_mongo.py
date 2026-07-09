"""
CRUD (Create, Read, Update, Delete) para as entidades:
usuario, estudante, curso, vinculo -- mapeadas em duas coleções MongoDB:

- "usuarios": documentos de usuário, com subdocumento embutido "estudante"
  (relação 1:1) contendo a lista embutida "vinculos" (relação 1:N).
- "cursos": coleção própria, referenciada pelo campo id_curso dentro de
  cada vínculo (relação N:1).

Uso: python crud_mongo.py   (executa uma demonstração no final do arquivo)
"""
from datetime import datetime
from bson import ObjectId
from mongo_db import get_db

db = get_db()


# ----------------------------------------------------------------------
# USUARIO
# ----------------------------------------------------------------------
def criar_usuario(nome, cpf, email, senha, data_nascimento):
    doc = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": senha,
        "data_nascimento": datetime.combine(data_nascimento, datetime.min.time())
        if not isinstance(data_nascimento, datetime) else data_nascimento,
    }
    resultado = db.usuarios.insert_one(doc)
    return resultado.inserted_id


def buscar_usuario(id_usuario=None):
    if id_usuario:
        return db.usuarios.find_one({"_id": ObjectId(id_usuario)})
    return list(db.usuarios.find())


def atualizar_usuario(id_usuario, **campos):
    if not campos:
        return False
    resultado = db.usuarios.update_one(
        {"_id": ObjectId(id_usuario)}, {"$set": campos}
    )
    return resultado.modified_count > 0


def deletar_usuario(id_usuario):
    resultado = db.usuarios.delete_one({"_id": ObjectId(id_usuario)})
    return resultado.deleted_count > 0


# ----------------------------------------------------------------------
# CURSO
# ----------------------------------------------------------------------
def criar_curso(codigo, nome, grau, departamento):
    doc = {"codigo": codigo, "nome": nome, "grau": grau, "departamento": departamento}
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


# ----------------------------------------------------------------------
# ESTUDANTE (subdocumento embutido dentro de usuarios, relação 1:1)
# ----------------------------------------------------------------------
def criar_estudante(id_usuario, matricula, data_ingresso):
    """Transforma um usuário existente em estudante, adicionando o
    subdocumento embutido com a lista de vínculos vazia."""
    doc = {
        "estudante.matricula": matricula,
        "estudante.data_ingresso": datetime.combine(data_ingresso, datetime.min.time())
        if not isinstance(data_ingresso, datetime) else data_ingresso,
        "estudante.vinculos": [],
    }
    resultado = db.usuarios.update_one({"_id": ObjectId(id_usuario)}, {"$set": doc})
    return resultado.modified_count > 0


def buscar_estudante(id_usuario=None):
    filtro = {"estudante": {"$ne": None}}
    if id_usuario:
        filtro["_id"] = ObjectId(id_usuario)
        return db.usuarios.find_one(filtro)
    return list(db.usuarios.find(filtro))


def atualizar_estudante(id_usuario, **campos):
    """campos deve usar as chaves matricula / data_ingresso."""
    if not campos:
        return False
    updates = {f"estudante.{k}": v for k, v in campos.items()}
    resultado = db.usuarios.update_one({"_id": ObjectId(id_usuario)}, {"$set": updates})
    return resultado.modified_count > 0


def deletar_estudante(id_usuario):
    """Remove o vínculo de 'ser estudante', mantendo o usuário base."""
    resultado = db.usuarios.update_one(
        {"_id": ObjectId(id_usuario)}, {"$unset": {"estudante": ""}}
    )
    return resultado.modified_count > 0


# ----------------------------------------------------------------------
# VINCULO (item dentro da lista embutida usuarios.estudante.vinculos)
# ----------------------------------------------------------------------
def criar_vinculo(id_usuario, id_curso, status, data_inicio, tipo_ingresso, data_fim=None):
    # Garante integridade referencial: o curso precisa existir
    if not db.cursos.find_one({"_id": ObjectId(id_curso)}):
        raise ValueError(f"Curso {id_curso} não existe.")

    id_vinculo = ObjectId()
    vinculo = {
        "id_vinculo": id_vinculo,
        "id_curso": ObjectId(id_curso),
        "status": status,
        "data_inicio": datetime.combine(data_inicio, datetime.min.time())
        if not isinstance(data_inicio, datetime) else data_inicio,
        "data_fim": data_fim,
        "tipo_ingresso": tipo_ingresso,
    }
    db.usuarios.update_one(
        {"_id": ObjectId(id_usuario)}, {"$push": {"estudante.vinculos": vinculo}}
    )
    return id_vinculo


def buscar_vinculo(id_usuario, id_vinculo=None):
    usuario = db.usuarios.find_one({"_id": ObjectId(id_usuario)})
    if not usuario or not usuario.get("estudante"):
        return None
    vinculos = usuario["estudante"].get("vinculos", [])
    if id_vinculo:
        return next((v for v in vinculos if v["id_vinculo"] == ObjectId(id_vinculo)), None)
    return vinculos


def atualizar_vinculo(id_usuario, id_vinculo, **campos):
    if not campos:
        return False
    updates = {f"estudante.vinculos.$.{k}": v for k, v in campos.items()}
    resultado = db.usuarios.update_one(
        {"_id": ObjectId(id_usuario), "estudante.vinculos.id_vinculo": ObjectId(id_vinculo)},
        {"$set": updates},
    )
    return resultado.modified_count > 0


def deletar_vinculo(id_usuario, id_vinculo):
    resultado = db.usuarios.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$pull": {"estudante.vinculos": {"id_vinculo": ObjectId(id_vinculo)}}},
    )
    return resultado.modified_count > 0


# ----------------------------------------------------------------------
# DEMONSTRAÇÃO
# ----------------------------------------------------------------------
if __name__ == "__main__":
    from datetime import date

    # 1. Cria um usuário
    id_u = criar_usuario("Maria Silva", "12345678901", "maria@ufs.br", "senha123", date(2003, 5, 14))
    print("Usuário criado:", buscar_usuario(id_u))

    # 2. Cria um curso
    id_c = criar_curso("CC-01", "Ciência da Computação", "Bacharelado", "DComp")
    print("Curso criado:", buscar_curso(id_c))

    # 3. Transforma o usuário em estudante
    criar_estudante(id_u, "202412345", date(2024, 3, 1))
    print("Estudante criado:", buscar_estudante(id_u))

    # 4. Cria o vínculo entre estudante e curso
    id_v = criar_vinculo(id_u, id_c, "ativo", date(2024, 3, 1), "sisu")
    print("Vínculo criado:", buscar_vinculo(id_u, id_v))

    # 5. Atualiza o vínculo
    atualizar_vinculo(id_u, id_v, status="trancado")
    print("Vínculo atualizado:", buscar_vinculo(id_u, id_v))

    # 6. Deleta o vínculo (não remove estudante nem curso)
    # deletar_vinculo(id_u, id_v)
