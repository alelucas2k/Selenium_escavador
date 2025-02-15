from datetime import datetime
from entity.ExperienciaProfissional import ExperienciaProfissional


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Este campo não pode ser vazio. Por favor, digite novamente.")

def get_valid_password(prompt):
    while True:
        value = input(prompt).strip()
        if len(value) >= 5:
            return value
        print("Este campo não pode ter menos que 5 caracteres. Por favor, digite novamente.")


def get_valid_number(prompt, min_val=None, max_val=None):
    while True:
        value = get_non_empty_input(prompt)
        if value.isdigit():
            num = int(value)
            if (min_val is None or num >= min_val) and (max_val is None or num <= max_val):
                return num
        print(
            f"Por favor, digite um número válido{' entre ' + str(min_val) + ' e ' + str(max_val) if min_val is not None and max_val is not None else ''}")


# def visualizar_professores():
#     from facade.facade import Facade
#
#     facade = Facade()
#     opcao = get_valid_number(
#         "\n\nComo você deseja visualizar os professores?\n\n"
#         "1. Todos os professores\n"
#         "2. Por área de conhecimento\n"
#         "3. Por projeto\n"
#         "Digite o número da opção: ", 1, 3
#     )
#
#     professores = facade.exibir_professores()
#
#     opcao = str(opcao)
#
#     if opcao == '1':
#         for professor in professores:
#             exibir_detalhes_professor(professor)
#     elif opcao == '2':
#         areas = facade.exibir_areas()
#         exibir_opcoes(areas, "Escolha a área de conhecimento")
#         area_index = obter_opcao_valida(areas)
#         selected_area = areas[int(area_index) - 1][1]
#
#         for professor in professores:
#             if selected_area in professor[5]:
#                 exibir_detalhes_professor(professor)
#     elif opcao == '3':
#         projetos = facade.exibir_projetos()
#         exibir_opcoes(projetos, "Digite o índice do projeto desejado")
#         proj_index = obter_opcao_valida(projetos)
#         selected_projeto = projetos[int(proj_index) - 1][1]
#
#         for professor in professores:
#             if selected_projeto in professor[6]:
#                 exibir_detalhes_professor(professor)
#     else:
#         print("Opção inválida. Tente novamente.")


def visualizar_professores():
    from facade.facade import Facade

    facade = Facade()
    opcao = get_valid_number(
        "\n\nComo você deseja visualizar os professores?\n\n"
        "1. Todos os professores\n"
        "2. Por área de conhecimento\n"
        "3. Por projeto\n"
        "Digite o número da opção: ", 1, 3
    )

    professores = facade.exibir_professores()

    opcao = str(opcao)

    if opcao == '1':
        for professor in professores:
            exibir_detalhes_professor(professor)
    elif opcao == '2':
        areas = facade.exibir_areas()
        exibir_opcoes(areas, "Escolha a área de conhecimento")
        area_index = obter_opcao_valida(areas)
        selected_area = areas[int(area_index) - 1][1]

        for professor in professores:
            if selected_area in professor[3]:
                exibir_detalhes_professor(professor)
    elif opcao == '3':
        projetos = facade.exibir_projetos()
        exibir_opcoes(projetos, "Digite o índice do projeto desejado")
        proj_index = obter_opcao_valida(projetos)
        selected_projeto = projetos[int(proj_index) - 1][1]

        for professor in professores:
            if selected_projeto in professor[4]:
                exibir_detalhes_professor(professor)
    else:
        print("Opção inválida. Tente novamente.")



def exibir_opcoes(opcoes, mensagem):
    print(mensagem)
    for opcao in opcoes:
        print(f'{opcao[0]}. {opcao[1]}')


def obter_opcao_valida(lista):
    opcao = input("Escolha uma opção: ")
    if not opcao.isdigit() or int(opcao) not in range(1, len(lista) + 1):
        print("Opção inválida, selecionando a primeira opção por padrão.")
        return '1'
    return opcao



def exibir_detalhes_aluno(aluno):
    print(f"\n\nID: {aluno[0]}")
    print(f"Nome: {aluno[1]}")
    print(f"Curso: {aluno[2]}")
    print(f"Email: {aluno[3]}")
    print(f"Período: {aluno[4]}")

    print(f"Senha: {aluno[5]}")

    if len(aluno[7]) >= 1:
        print(f"Áreas de interesse: {', '.join(aluno[7])}")

    if len(aluno[8]) >= 1:
        print(f"Projetos: {', '.join(aluno[8])}")

    # Exibindo estágios (se houver)
    if aluno[6]:
        print("Estágios:")
        for estagio in aluno[6]:
            print(f"  ID: {estagio['id']}")
            print(f"  Título: {estagio['titulo']}")
            print(f"  Data de Início: {estagio['data_inicio']}")
            print(f"  Data de Fim: {estagio['data_fim']}")
            print(f"  Descrição: {estagio['descricao']}\n")

    print("-" * 40)


def visualizar_alunos():
    from facade.facade import Facade

    opcao = get_valid_number(
        "Como você deseja visualizar os alunos?\n\n"
        "1. Todos os alunos\n"
        "2. Por área de interesse\n"
        "3. Por curso\n"
        "4. Por projeto participado\n\n"
        "Digite o número da opção: ", 1, 4
    )
    facade = Facade()
    opcao = str(opcao)
    alunos = facade.exibir_alunos(str(opcao))

    if opcao == '1':
        for aluno in alunos:
            exibir_detalhes_aluno(aluno)
    elif opcao == '2':
        areas = facade.exibir_areas()
        exibir_opcoes(areas, "Escolha a área de interesse")
        area_index = obter_opcao_valida(areas)
        selected_area = areas[int(area_index) - 1][1]

        for aluno in alunos:
            if selected_area in aluno[7]:
                exibir_detalhes_aluno(aluno)
    elif opcao == '3':
        cursos = facade.exibir_cursos()
        exibir_opcoes(cursos, "Digite o índice do curso desejado")
        curso_index = obter_opcao_valida(cursos)
        selected_curso = cursos[int(curso_index) - 1][1]

        for aluno in alunos:
            if selected_curso == aluno[2]:
                exibir_detalhes_aluno(aluno)
    elif opcao == '4':
        projetos = facade.exibir_projetos()
        exibir_opcoes(projetos, "Digite o índice do projeto desejado")
        proj_index = obter_opcao_valida(projetos)
        selected_projeto = projetos[int(proj_index) - 1][1]

        for aluno in alunos:
            if selected_projeto in aluno[8]:
                exibir_detalhes_aluno(aluno)
    else:
        print("Opção inválida. Tente novamente.")


def inserir_areas_interesse():
    from facade.facade import Facade
    facade = Facade()

    areas = facade.exibir_areas()
    for area in areas:
        print(f'{area[0]}. {area[1]}')

    while True:
        areas_input = input("Digite o número das suas áreas de interesse, separe por espaços:\n")
        areas_selecionadas = [int(numero) for numero in areas_input.split() if numero.isdigit()]
        return areas_selecionadas

def apagar_areas_interesse():
    from facade.facade import Facade
    facade = Facade()

    areas = facade.exibir_areas()
    for area in areas:
        print(f'{area[0]}. {area[1]}')

    while True:
        areas_input = get_non_empty_input("Digite o número das áreas que deseja excluir, separe por espaços:\n")
        areas_selecionadas = [int(numero) for numero in areas_input.split() if numero.isdigit()]
        if areas_selecionadas:
            return areas_selecionadas
        print("Nenhuma área válida selecionada. Tente novamente.")


def cadastrar_aluno():
    from facade.facade import Facade
    facade = Facade()

    cursos = ['engenharia de computação', 'telemática', 'técnico em informática']
    experiencias_profissionais = []

    # Nome
    while True:
        nome = get_non_empty_input("\nDigite seu nome completo: ")
        if input(f"Seu nome é '{nome}'? (digite y para confirmar): ").lower() == 'y':
            break

    # Curso
    curso = get_valid_number(
        f"\nSelecione o seu curso:\n1. Engenharia de Computação\n2. Telemática\n3. Técnico em Informática\n",
        1, 3
    )

    # Email
    while True:
        email_part = get_non_empty_input("\nDigite seu email academico sem o domínio (@academico.ifpb.edu.br): ")
        email = email_part + '@academico.ifpb.edu.br'
        if input(f"Seu email é '{email}'? (digite y para confirmar): ").lower() == 'y':
            break

    # Período
    periodo = get_valid_number("\nDigite o período em que você está matriculado: ", 1, 10)

    # Senha
    while True:
        senha1 = get_valid_password("\nDigite a senha desejada: ")
        senha2 = get_valid_password("\nConfirme sua senha: ")
        if senha1 == senha2:
            break
        print("\n*As senhas não coincidem*\n")

    # Experiências Profissionais
    print("\n\nAgora vamos cadastrar seus interesses e experiências.\n")
    while True:

        if input("\nDeseja inserir (outra) experiência? (y/n): ").lower() != 'y':
            break


        titulo = get_non_empty_input("\nInsira o título da experiência profissional: ")

        # Data de início
        data_inicio_dt = None
        while not data_inicio_dt:
            try:
                dia_inicio = get_non_empty_input("Informe o dia da data de início: ")
                mes_inicio = get_non_empty_input("Informe o mês da data de início: ")
                ano_inicio = get_non_empty_input("Informe o ano da data de início: ")
                data_inicio = f"{dia_inicio}/{mes_inicio}/{ano_inicio}"
                data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
            except ValueError:
                print("Data inválida. Tente novamente.")

        # Data final
        data_fim_dt = None
        while not data_fim_dt:
            try:
                dia_fim = get_non_empty_input("Informe o dia da data final: ")
                mes_fim = get_non_empty_input("Informe o mês da data final: ")
                ano_fim = get_non_empty_input("Informe o ano da data final: ")
                data_fim = f"{dia_fim}/{mes_fim}/{ano_fim}"
                data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")
            except ValueError:
                print("Data inválida. Tente novamente.")

        descricao = get_non_empty_input("Insira um breve texto de descrição da sua experiência:\n")

        experiencias_profissionais.append(
            ExperienciaProfissional(None, titulo, data_inicio_dt, data_fim_dt, descricao)
        )


    # Áreas de Interesse
    print("\nCadastre suas áreas de interesse:")
    areas_interesse = inserir_areas_interesse()

    # Projetos
    print('\nPor último, selecione os projetos participados:')
    projetos = inserir_projetos()

    facade.criar_aluno(nome, cursos[curso - 1], email, str(periodo), senha1, experiencias_profissionais,
                       areas_interesse, projetos)


def inserir_projetos():
    from facade.facade import Facade
    facade = Facade()

    projetos = facade.exibir_projetos()
    for projeto in projetos:
        print(f'{projeto[0]}. {projeto[1]}')

    while True:
        projetos_input = input("Digite o número dos projetos que já participou, separe por espaços:\n")
        proj_selecionados = [int(numero) for numero in projetos_input.split() if numero.isdigit()]
        return proj_selecionados


def apagar_projetos():
    from facade.facade import Facade
    facade = Facade()

    projetos = facade.exibir_projetos()
    for projeto in projetos:
        print(f'{projeto[0]}. {projeto[1]}')

    while True:
        projetos_input = get_non_empty_input("Digite o número dos projetos que deseja apagar, separe por espaços:\n")
        proj_selecionados = [int(numero) for numero in projetos_input.split() if numero.isdigit()]
        if proj_selecionados:
            return proj_selecionados
        print("Nenhum projeto válido selecionado. Tente novamente.")


def editar_vitrine():
    from facade.facade import Facade
    from repository.login import LoginProxy

    cursos = ['engenharia de computação', 'telemática', 'técnico em informática']
    facade = Facade()
    proxy = LoginProxy()

    # Autenticação
    while True:
        email = get_non_empty_input("Digite seu email: ")
        senha = get_non_empty_input("Digite sua senha: ")
        resultado = proxy.autenticar(email, senha)
        if resultado["status"] == "success":
            print(f"Bem-vindo {resultado['dados'][1]} ({resultado['tipo']})!\n")
            break
        print(resultado["message"] + "\n")

    # Menu de edição
    while True:
        opcao = get_valid_number(
            "\nSelecione uma opção:\n"
            "(1) Visualizar sua vitrine\n(2) Editar Nome\n(3) Editar Curso\n"
            "(4) Editar Período\n(5) Editar Senha\n(6) Inserir Experiência\n"
            "(7) Apagar Experiência\n(8) Inserir Áreas\n(9) Apagar Áreas\n"
            "(10) Inserir Projetos\n(11) Apagar Projetos\n(12) Sair\nOpção: ", 1, 12
        )

        if opcao == 1:
            aluno = facade.exibir_aluno(email)
            exibir_detalhes_aluno(aluno)
        elif opcao == 2:
            novo_nome = get_non_empty_input("Digite o novo nome: ")
            facade.update_nome_by_email(email, novo_nome)
        elif opcao == 3:
            novo_curso = get_valid_number(
                f"\nSelecione o curso:\n1. Engenharia de Computação\n2. Telemática\n3. Técnico em Informática\n",
                1, 3
            )
            facade.update_curso_by_email(email, cursos[novo_curso - 1])
        elif opcao == 4:
            novo_periodo = get_valid_number("\nDigite o novo período: ", 1, 100)
            facade.update_periodo_by_email(email, str(novo_periodo))
        elif opcao == 5:
            while True:
                nova_senha = get_valid_password("\nNova senha: ")
                confirmacao = get_valid_password("Confirme a senha: ")
                if nova_senha == confirmacao:
                    facade.update_senha_by_email(email, nova_senha)
                    break
                print("\nAs senhas não coincidem!")
        elif opcao == 6:
            while True:
                if input("\nAdicionar experiência? (y/n): ").lower() != 'y':
                    break
                titulo = get_non_empty_input("\nTítulo da experiência: ")

                # Data de início
                data_inicio = None
                while not data_inicio:
                    try:
                        dia = get_non_empty_input("Dia de início: ")
                        mes = get_non_empty_input("Mês de início: ")
                        ano = get_non_empty_input("Ano de início: ")
                        data_inicio = f"{dia}/{mes}/{ano}"
                        datetime.strptime(data_inicio, "%d/%m/%Y")
                    except ValueError:
                        print("Data inválida!")

                # Data final
                data_fim = None
                while not data_fim:
                    try:
                        dia = get_non_empty_input("Dia final: ")
                        mes = get_non_empty_input("Mês final: ")
                        ano = get_non_empty_input("Ano final: ")
                        data_fim = f"{dia}/{mes}/{ano}"
                        datetime.strptime(data_fim, "%d/%m/%Y")
                    except ValueError:
                        print("Data inválida!")

                descricao = get_non_empty_input("Descrição: ")
                facade.criar_experiencia_profissional_aluno_by_email(email, titulo, data_inicio, data_fim, descricao)

        elif opcao == 7:
            experiencia_id = get_valid_number("\nID da experiência para apagar: ", 1)
            facade.apagar_experiencia(str(experiencia_id))
        elif opcao == 8:
            areas = inserir_areas_interesse()
            facade.inserir_areas_interesse_por_email(email, areas)
        elif opcao == 9:
            areas = apagar_areas_interesse()
            facade.apagar_area_interesse_por_email(email, areas)
        elif opcao == 10:
            projetos = inserir_projetos()
            facade.inserir_projeto_participado_por_email(email, projetos)
        elif opcao == 11:
            projetos = apagar_projetos()
            facade.apagar_projeto_participado_por_email(email, projetos)
        else:
            break


def inserir_sugestao_professor():
    from facade.facade import Facade
    facade = Facade()

    nome = get_non_empty_input("\nDigite o nome do professor a sugerir: ")
    facade.inserir_sugestao_professor(nome)


def exibir_detalhes_professor(professor):
    print(f"\n\nID: {professor[0]}")
    print(f"Nome: {professor[1]}")
    print(f"Resumo: {professor[2]}")
    print(f"Áreas de conhecimento: {', '.join(professor[3])}")
    print(f"Projetos: {', '.join(professor[4])}")
    print("-" * 40)


def interface():
    print("**********************************")
    print("        BEM-VINDO                 ")
    print("**********************************\n")

    while True:
        opcao = get_valid_number(
            "Selecione uma opção:\n"
            "(1) Visualizar professores\n(2) Visualizar alunos\n"
            "(3) Cadastrar vitrine\n(4) Editar vitrine\n"
            "(5) Sugerir professor\n(6) Sair\nOpção: ", 1, 6
        )

        if opcao == 1:
            visualizar_professores()
        elif opcao == 2:
            visualizar_alunos()
        elif opcao == 3:
            cadastrar_aluno()
        elif opcao == 4:
            editar_vitrine()
        elif opcao == 5:
            inserir_sugestao_professor()
        else:
            print("\nAté logo!")
            break