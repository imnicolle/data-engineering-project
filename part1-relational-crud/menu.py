"""
Interface de linha de comando (menu interativo) para o CRUD relacional.
Este módulo cuida apenas da interação com o usuário (ler entradas,
chamar as operações do crud.py, e mandar o resultado para o exibicao.py).
Não contém lógica de acesso ao banco nem formatação de saída.

Uso: python menu.py
"""
import crud
import exibicao


def pausa():
    input("\nPressione Enter para continuar...")


def ler_opcional(prompt):
    valor = input(prompt).strip()
    return valor if valor else None

# MENU: USUARIO

def menu_usuario():
    while True:
        print("\n--- USUÁRIO ---")
        print("1. Criar usuário")
        print("2. Buscar usuário (por CPF)")
        print("3. Listar todos os usuários")
        print("4. Atualizar usuário")
        print("5. Deletar usuário")
        print("0. Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            cpf = input("CPF: ").strip()
            nome = input("Nome: ").strip()
            nascimento = ler_opcional("Data de nascimento (AAAA-MM-DD) [opcional]: ")
            email = ler_opcional("E-mail [opcional]: ")
            telefone = ler_opcional("Telefone [opcional]: ")
            login = ler_opcional("Login [opcional]: ")
            senha = ler_opcional("Senha [opcional]: ")
            crud.criar_usuario(cpf, nome, nascimento, email=[email] if email else None,
                                telefone=[telefone] if telefone else None,
                                login=login, senha=senha)
            exibicao.exibir_resultado(True, "Usuário criado com sucesso!")

        elif op == "2":
            cpf = input("CPF a buscar: ").strip()
            exibicao.exibir_usuario(crud.buscar_usuario(cpf))

        elif op == "3":
            exibicao.exibir_usuarios(crud.buscar_usuario())

        elif op == "4":
            cpf = input("CPF do usuário a atualizar: ").strip()
            campo = input("Campo a atualizar (nome/email/telefone/data_nascimento/login/senha): ").strip()
            valor = input("Novo valor: ").strip()
            if campo in ("email", "telefone"):
                valor = [valor]  # o banco espera uma lista
            ok = crud.atualizar_usuario(cpf, **{campo: valor})
            exibicao.exibir_resultado(ok, "Usuário atualizado com sucesso!")

        elif op == "5":
            cpf = input("CPF do usuário a deletar: ").strip()
            ok = crud.deletar_usuario(cpf)
            exibicao.exibir_resultado(ok, "Usuário deletado com sucesso!")

        elif op == "0":
            break
        else:
            print("Opção inválida.")
        pausa()

# MENU: CURSO

def menu_curso():
    while True:
        print("\n--- CURSO ---")
        print("1. Criar curso")
        print("2. Buscar curso (por ID)")
        print("3. Listar todos os cursos")
        print("4. Atualizar curso")
        print("5. Deletar curso")
        print("0. Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            nome = input("Nome do curso: ").strip()
            grau = input("Grau (Bacharelado/Licenciatura Plena): ").strip()
            turno = input("Turno (Matutino/Vespertino/Noturno/Turno Indefinido): ").strip()
            campus = ler_opcional("Campus [opcional]: ")
            nivel = ler_opcional("Nível (Graduação/Mestrado/Doutorado/Lato) [opcional]: ")
            id_c = crud.criar_curso(nome, grau, turno, campus, nivel)
            exibicao.exibir_resultado(True, f"Curso criado com sucesso! ID: {id_c}")

        elif op == "2":
            id_c = input("ID do curso a buscar: ").strip()
            exibicao.exibir_curso(crud.buscar_curso(int(id_c)))

        elif op == "3":
            exibicao.exibir_cursos(crud.buscar_curso())

        elif op == "4":
            id_c = input("ID do curso a atualizar: ").strip()
            campo = input("Campo a atualizar (nome/grau/turno/campus/nivel): ").strip()
            valor = input("Novo valor: ").strip()
            ok = crud.atualizar_curso(int(id_c), **{campo: valor})
            exibicao.exibir_resultado(ok, "Curso atualizado com sucesso!")

        elif op == "5":
            id_c = input("ID do curso a deletar: ").strip()
            ok = crud.deletar_curso(int(id_c))
            exibicao.exibir_resultado(ok, "Curso deletado com sucesso!")

        elif op == "0":
            break
        else:
            print("Opção inválida.")
        pausa()

# MENU: ESTUDANTE

def menu_estudante():
    while True:
        print("\n--- ESTUDANTE ---")
        print("1. Transformar usuário em estudante")
        print("2. Buscar estudante (por matrícula)")
        print("3. Listar todos os estudantes")
        print("4. Atualizar estudante")
        print("5. Deletar estudante (remove só o vínculo de estudante)")
        print("0. Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            mat = input("Matrícula (até 7 caracteres): ").strip()
            cpf = input("CPF do usuário já existente: ").strip()
            mc = ler_opcional("MC [opcional]: ")
            ano = ler_opcional("Ano de ingresso [opcional]: ")
            crud.criar_estudante(mat, cpf, mc=float(mc) if mc else None,
                                  ano_ingresso=int(ano) if ano else None)
            exibicao.exibir_resultado(True, "Estudante criado com sucesso!")

        elif op == "2":
            mat = input("Matrícula a buscar: ").strip()
            exibicao.exibir_estudante(crud.buscar_estudante(mat))

        elif op == "3":
            exibicao.exibir_estudantes(crud.buscar_estudante())

        elif op == "4":
            mat = input("Matrícula do estudante a atualizar: ").strip()
            campo = input("Campo a atualizar (mc/ano_ingresso): ").strip()
            valor = input("Novo valor: ").strip()
            ok = crud.atualizar_estudante(mat, **{campo: valor})
            exibicao.exibir_resultado(ok, "Estudante atualizado com sucesso!")

        elif op == "5":
            mat = input("Matrícula do estudante a deletar: ").strip()
            ok = crud.deletar_estudante(mat)
            exibicao.exibir_resultado(ok, "Estudante deletado com sucesso!")

        elif op == "0":
            break
        else:
            print("Opção inválida.")
        pausa()

# MENU: VINCULO

def menu_vinculo():
    while True:
        print("\n--- VÍNCULO ---")
        print("1. Criar vínculo")
        print("2. Buscar vínculo (por ID)")
        print("3. Listar todos os vínculos")
        print("4. Atualizar vínculo")
        print("5. Deletar vínculo")
        print("0. Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            mat = input("Matrícula do estudante: ").strip()
            curso = input("ID do curso: ").strip()
            status = input("Status (Ativo/Cancelada/Formando/Graduado): ").strip()
            data_entrada = ler_opcional("Data de entrada (AAAA-MM-DD) [opcional]: ")
            id_v = crud.criar_vinculo(mat, int(curso), status, data_entrada)
            exibicao.exibir_resultado(True, f"Vínculo criado com sucesso! ID: {id_v}")

        elif op == "2":
            id_v = input("ID do vínculo a buscar: ").strip()
            exibicao.exibir_vinculo(crud.buscar_vinculo(int(id_v)))

        elif op == "3":
            exibicao.exibir_vinculos(crud.buscar_vinculo())

        elif op == "4":
            id_v = input("ID do vínculo a atualizar: ").strip()
            campo = input("Campo a atualizar (status/data_saida): ").strip()
            valor = input("Novo valor: ").strip()
            ok = crud.atualizar_vinculo(int(id_v), **{campo: valor})
            exibicao.exibir_resultado(ok, "Vínculo atualizado com sucesso!")

        elif op == "5":
            id_v = input("ID do vínculo a deletar: ").strip()
            ok = crud.deletar_vinculo(int(id_v))
            exibicao.exibir_resultado(ok, "Vínculo deletado com sucesso!")

        elif op == "0":
            break
        else:
            print("Opção inválida.")
        pausa()

# MENU PRINCIPAL

def main():
    while True:
        print("\n===== CRUD RELACIONAL - Esquema Universidade =====")
        print("1. Usuário")
        print("2. Curso")
        print("3. Estudante")
        print("4. Vínculo")
        print("0. Sair")
        op = input("Escolha uma entidade: ").strip()

        if op == "1":
            menu_usuario()
        elif op == "2":
            menu_curso()
        elif op == "3":
            menu_estudante()
        elif op == "4":
            menu_vinculo()
        elif op == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()