"""
Módulo de exibição (view). Responsável apenas por formatar e imprimir
os dados na tela -- não contém nenhuma lógica de acesso ao banco.
"""


def exibir_usuario(usuario):
    if not usuario:
        print("Usuário não encontrado.")
        return
    print("-" * 40)
    print(f"CPF:             {usuario.get('cpf')}")
    print(f"Nome:            {usuario.get('nome')}")
    print(f"Data nascimento: {usuario.get('data_nascimento')}")
    print(f"E-mail:          {usuario.get('email')}")
    print(f"Telefone:        {usuario.get('telefone')}")
    print(f"Login:           {usuario.get('login')}")
    print("-" * 40)


def exibir_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        exibir_usuario(u)


def exibir_curso(curso):
    if not curso:
        print("Curso não encontrado.")
        return
    print("-" * 40)
    print(f"ID:     {curso.get('idcurso')}")
    print(f"Nome:   {curso.get('nome')}")
    print(f"Grau:   {curso.get('grau')}")
    print(f"Turno:  {curso.get('turno')}")
    print(f"Campus: {curso.get('campus')}")
    print(f"Nível:  {curso.get('nivel')}")
    print("-" * 40)


def exibir_cursos(cursos):
    if not cursos:
        print("Nenhum curso cadastrado.")
        return
    for c in cursos:
        exibir_curso(c)


def exibir_estudante(estudante):
    if not estudante:
        print("Estudante não encontrado.")
        return
    print("-" * 40)
    print(f"Matrícula:    {estudante.get('mat_estudante')}")
    print(f"Nome:         {estudante.get('nome')}")
    print(f"MC:           {estudante.get('mc')}")
    print(f"Ano ingresso: {estudante.get('ano_ingresso')}")
    print("-" * 40)


def exibir_estudantes(estudantes):
    if not estudantes:
        print("Nenhum estudante cadastrado.")
        return
    for e in estudantes:
        exibir_estudante(e)


def exibir_vinculo(vinculo):
    if not vinculo:
        print("Vínculo não encontrado.")
        return
    print("-" * 40)
    print(f"ID:            {vinculo.get('idvinculo')}")
    print(f"Matrícula:     {vinculo.get('mat_estudante')}")
    print(f"Curso (ID):    {vinculo.get('curso')}")
    print(f"Status:        {vinculo.get('status')}")
    print(f"Data entrada:  {vinculo.get('data_entrada')}")
    print(f"Data saída:    {vinculo.get('data_saida')}")
    print("-" * 40)


def exibir_vinculos(vinculos):
    if not vinculos:
        print("Nenhum vínculo cadastrado.")
        return
    for v in vinculos:
        exibir_vinculo(v)


def exibir_resultado(sucesso, mensagem_sucesso, mensagem_falha="Nenhum registro encontrado."):
    print(mensagem_sucesso if sucesso else mensagem_falha)
