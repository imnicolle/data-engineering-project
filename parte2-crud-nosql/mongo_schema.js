// Script de criação das coleções NoSQL (MongoDB)
// Estrutura baseada no esquema "universidade" trabalhado em aula.
// Execute no mongosh, ou cole no shell embutido do MongoDB Compass.
// Mapeamento: usuario/estudante -> embutido (1:1) | estudante/vinculo -> embutido (1:N)
//             curso -> coleção própria, referenciada por vinculo (N:1)

use bancoufs_nosql;

// Coleção: cursos

db.createCollection("cursos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nome", "turno"],
      properties: {
        nome: { bsonType: "string", description: "obrigatório" },
        grau: {
          enum: ["Bacharelado", "Licenciatura Plena", null],
          description: "restrição de domínio"
        },
        turno: {
          enum: ["Matutino", "Vespertino", "Noturno", "Turno Indefinido"],
          description: "obrigatório, restrição de domínio"
        },
        campus: { bsonType: ["string", "null"] },
        nivel: {
          enum: ["Graduação", "Mestrado", "Doutorado", "Lato", null],
          description: "restrição de domínio"
        }
      }
    }
  }
});

// Chave natural composta (equivalente ao UNIQUE(nome, turno, campus, nivel) do relacional)
db.cursos.createIndex(
  { nome: 1, turno: 1, campus: 1, nivel: 1 },
  { unique: true }
);

// Coleção: usuarios (com subdocumento embutido "estudante")
// Chave: cpf (equivalente à chave primária do relacional)

db.createCollection("usuarios", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cpf", "nome"],
      properties: {
        cpf: { bsonType: "string", description: "obrigatório, único (chave natural)" },
        nome: { bsonType: "string" },
        data_nascimento: { bsonType: ["date", "null"] },
        email: {
          bsonType: ["array", "null"],
          items: { bsonType: "string" }
        },
        telefone: {
          bsonType: ["array", "null"],
          items: { bsonType: "string" }
        },
        login: { bsonType: ["string", "null"] },
        senha: { bsonType: ["string", "null"] },
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
                  status: {
                    enum: ["Ativo", "Cancelada", "Formando", "Graduado"]
                  },
                  data_entrada: { bsonType: ["date", "null"] },
                  data_saida: { bsonType: ["date", "null"] }
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
// Índice único parcial: só aplica quando o campo existe (nem todo usuário é estudante)
db.usuarios.createIndex(
  { "estudante.mat_estudante": 1 },
  { unique: true, partialFilterExpression: { "estudante.mat_estudante": { $exists: true } } }
);