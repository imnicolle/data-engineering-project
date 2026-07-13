// Script de criação das coleções NoSQL (MongoDB)
// Mapeamento COMPLETO do esquema "universidade" trabalhado em aula.
// Execute no mongosh, ou cole em blocos pequenos no shell do MongoDB Compass.
//
// Observação: o CRUD implementado em Python (crud_mongo.py) manipula apenas
// usuarios/cursos (entidades usuário, estudante, vínculo, curso), conforme
// pedido no enunciado. As demais coleções abaixo (departamentos, disciplinas,
// semestres, projetos, turmas) existem apenas para fins de representação/
// mapeamento (item "Mapeamento: Todas as tabelas devem ser representadas
// no NoSQL"), sem CRUD associado.
//
// Mapeamento relacional -> MongoDB:
//   usuario + estudante + professor -> embutidos em "usuarios" (relação 1:1)
//   vinculo, turmas_cursadas, planos -> listas embutidas dentro de "estudante" (1:N)
//   curso, departamento, disciplina, semestre, projeto -> coleções próprias
//   leciona (turma-professor) e alocacao (turma-sala-horario) -> embutidos em "turmas"

use bancoufs_nosql;

// Coleção: cursos

db.createCollection("cursos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nome", "turno"],
      properties: {
        nome: { bsonType: "string", description: "obrigatório" },
        grau: { enum: ["Bacharelado", "Licenciatura Plena", null] },
        turno: {
          enum: ["Matutino", "Vespertino", "Noturno", "Turno Indefinido"],
          description: "obrigatório, restrição de domínio"
        },
        campus: { bsonType: ["string", "null"] },
        nivel: { enum: ["Graduação", "Mestrado", "Doutorado", "Lato", null] }
      }
    }
  }
});
db.cursos.createIndex(
  { nome: 1, turno: 1, campus: 1, nivel: 1 },
  { unique: true }
);

// Coleção: usuarios (com subdocumentos embutidos "estudante" e "professor")
// Chave natural: cpf

db.createCollection("usuarios", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cpf", "nome"],
      properties: {
        cpf: { bsonType: "string", description: "obrigatório, único (chave natural)" },
        nome: { bsonType: "string" },
        data_nascimento: { bsonType: ["date", "null"] },
        email: { bsonType: ["array", "null"], items: { bsonType: "string" } },
        telefone: { bsonType: ["array", "null"], items: { bsonType: "string" } },
        login: { bsonType: ["string", "null"] },
        senha: { bsonType: ["string", "null"] },
        professor: {
          bsonType: ["object", "null"],
          description: "subdocumento 1:1 - null se o usuário não for professor",
          properties: {
            mat_professor: { bsonType: "string" },
            departamento: { bsonType: ["string", "null"], description: "referência a departamentos.cod_depto" },
            formacao: { enum: ["Graduação", "Especialização", "Mestrado", "Doutorado", null] },
            data_admissao: { bsonType: ["date", "null"] },
            tipo_jornada_trabalho: { enum: ["20h", "40h", "DE", null] },
            salario: { bsonType: ["double", "null"] }
          }
        },
        estudante: {
          bsonType: ["object", "null"],
          description: "subdocumento 1:1 - null se o usuário não for estudante",
          properties: {
            mat_estudante: { bsonType: "string" },
            mc: { bsonType: ["double", "int", "null"] },
            ano_ingresso: { bsonType: ["int", "null"] },
            vinculos: {
              bsonType: "array",
              description: "lista embutida 1:N de vínculos com cursos",
              items: {
                bsonType: "object",
                required: ["id_curso", "status"],
                properties: {
                  id_vinculo: { bsonType: "objectId" },
                  id_curso: { bsonType: "objectId", description: "referência à coleção cursos" },
                  status: { enum: ["Ativo", "Cancelada", "Formando", "Graduado"] },
                  data_entrada: { bsonType: ["date", "null"] },
                  data_saida: { bsonType: ["date", "null"] }
                }
              }
            },
            turmas_cursadas: {
              bsonType: "array",
              description: "equivalente à tabela cursa (N:N estudante-turma, com nota)",
              items: {
                bsonType: "object",
                properties: {
                  id_turma: { bsonType: "objectId" },
                  nota: { bsonType: ["double", "null"] }
                }
              }
            },
            planos: {
              bsonType: "array",
              description: "equivalente à tabela plano (projeto + professor + ano)",
              items: {
                bsonType: "object",
                properties: {
                  id_projeto: { bsonType: "int" },
                  mat_professor: { bsonType: ["string", "null"] },
                  ano: { bsonType: "int" }
                }
              }
            }
          }
        }
      }
    }
  }
});
db.usuarios.createIndex({ cpf: 1 }, { unique: true });
db.usuarios.createIndex({ login: 1 }, { unique: true, partialFilterExpression: { login: { $exists: true } } });
db.usuarios.createIndex(
  { "estudante.mat_estudante": 1 },
  { unique: true, partialFilterExpression: { "estudante.mat_estudante": { $exists: true } } }
);

// Coleção: departamentos

db.createCollection("departamentos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cod_depto", "nome"],
      properties: {
        cod_depto: { bsonType: "string" },
        nome: { bsonType: "string" },
        chefe_mat_professor: { bsonType: ["string", "null"], description: "referência ao professor chefe" },
        orcamento: { bsonType: ["double", "null"] },
        comissal: { bsonType: ["double", "null"] }
      }
    }
  }
});
db.departamentos.createIndex({ cod_depto: 1 }, { unique: true });


// Coleção: disciplinas

db.createCollection("disciplinas", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cod_disc", "nome"],
      properties: {
        cod_disc: { bsonType: "string" },
        nome: { bsonType: "string" },
        pre_req: { bsonType: ["string", "null"], description: "auto-referência a outra disciplina" },
        creditos: { bsonType: ["int", "null"] },
        depto_responsavel: { bsonType: ["string", "null"], description: "referência a departamentos.cod_depto" }
      }
    }
  }
});
db.disciplinas.createIndex({ cod_disc: 1 }, { unique: true });

// Coleção: semestres

db.createCollection("semestres", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["ano", "semestre"],
      properties: {
        ano: { bsonType: "int" },
        semestre: { bsonType: "int" },
        data_inicio: { bsonType: ["date", "null"] },
        data_fim: { bsonType: ["date", "null"] }
      }
    }
  }
});
db.semestres.createIndex({ ano: 1, semestre: 1 }, { unique: true });

// Coleção: projetos

db.createCollection("projetos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id_projeto"],
      properties: {
        id_projeto: { bsonType: "int" },
        descricao: { bsonType: ["string", "null"] }
      }
    }
  }
});
db.projetos.createIndex({ id_projeto: 1 }, { unique: true });

// Coleção: turmas
// Embute: professores que lecionam (leciona) e as alocações de sala/horário

db.createCollection("turmas", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cod_disc", "ano", "semestre"],
      properties: {
        cod_disc: { bsonType: "string", description: "referência a disciplinas.cod_disc" },
        numero: { bsonType: ["int", "null"] },
        ano: { bsonType: "int" },
        semestre: { bsonType: "int" },
        professores: {
          bsonType: "array",
          description: "equivalente à tabela leciona (N:N turma-professor)",
          items: { bsonType: "string", description: "mat_professor" }
        },
        alocacoes: {
          bsonType: "array",
          description: "equivalente às tabelas sala/horario/alocacao",
          items: {
            bsonType: "object",
            properties: {
              dia: { bsonType: "string" },
              slot: { bsonType: "int" },
              sala_descricao: { bsonType: "string" }
            }
          }
        }
      }
    }
  }
});
db.turmas.createIndex({ cod_disc: 1, numero: 1, ano: 1, semestre: 1 }, { unique: true });