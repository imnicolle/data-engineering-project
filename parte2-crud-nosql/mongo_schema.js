// Script de criação do esquema NoSQL (MongoDB)
// Execute no mongosh, ou cole no "Mongosh" embutido do MongoDB Compass.
// Mapeamento: usuario/estudante -> embutido (1:1) | estudante/vinculo -> embutido (1:N)
//             curso -> coleção própria, referenciada por vinculo (N:1)

use bancoufs_nosql;

// -----------------------------------------------------
// Coleção: cursos
// -----------------------------------------------------
db.createCollection("cursos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["codigo", "nome", "grau", "departamento"],
      properties: {
        codigo: { bsonType: "string", description: "obrigatório, único" },
        nome: { bsonType: "string", description: "obrigatório" },
        grau: {
          enum: ["Bacharelado", "Licenciatura", "Tecnologo"],
          description: "obrigatório, restrição de domínio"
        },
        departamento: { bsonType: "string", description: "obrigatório" }
      }
    }
  }
});

db.cursos.createIndex({ codigo: 1 }, { unique: true });

// -----------------------------------------------------
// Coleção: usuarios (com subdocumento embutido "estudante")
// -----------------------------------------------------
db.createCollection("usuarios", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nome", "cpf", "email", "senha", "data_nascimento"],
      properties: {
        nome: { bsonType: "string" },
        cpf: { bsonType: "string", description: "obrigatório, único, 11 dígitos" },
        email: { bsonType: "string", description: "obrigatório, único" },
        senha: { bsonType: "string" },
        data_nascimento: { bsonType: "date" },
        estudante: {
          bsonType: ["object", "null"],
          description: "subdocumento 1:1 - null se o usuário não for estudante",
          properties: {
            matricula: { bsonType: "string" },
            data_ingresso: { bsonType: "date" },
            vinculos: {
              bsonType: "array",
              description: "lista embutida 1:N de vínculos com cursos",
              items: {
                bsonType: "object",
                required: ["id_curso", "status", "data_inicio", "tipo_ingresso"],
                properties: {
                  id_vinculo: { bsonType: "objectId" },
                  id_curso: { bsonType: "objectId", description: "referência à coleção cursos" },
                  status: {
                    enum: ["ativo", "trancado", "formado", "cancelado", "transferido"]
                  },
                  data_inicio: { bsonType: "date" },
                  data_fim: { bsonType: ["date", "null"] },
                  tipo_ingresso: {
                    enum: ["vestibular", "sisu", "transferencia", "reopcao", "outro"]
                  }
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
db.usuarios.createIndex({ email: 1 }, { unique: true });
// Índice único parcial: só aplica a restrição quando o campo existe
// (nem todo usuário é estudante)
db.usuarios.createIndex(
  { "estudante.matricula": 1 },
  { unique: true, partialFilterExpression: { "estudante.matricula": { $exists: true } } }
);
