import ClassSeller
from ClassSeller import SellerManagement
import os
import random
import string
from datetime import datetime, timedelta


# As funções abaixo são apenas para automação de testes


def generate_name() -> str:
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'William', 'Jessica',
                   'David', 'Emily', 'Robert', 'Linda']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
                  'Miller', 'Davis', 'Rodriguez', 'Martinez']
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"


def generate_UF() -> str:
    first_letter = ['S', 'S', 'G', 'M', 'B',]
    second_letter = ['C', 'P', 'O', 'G', 'A',]
    one = random.choice(first_letter)
    two = random.choice(second_letter)
    return f"{one}{two}"


def generate_data(
        start_date: str = '1925-01-01',
        end_date: str = '2020-12-31') -> str:

    formato_data = '%Y-%m-%d'
    data_inicio = datetime.strptime(start_date, formato_data)
    data_fim = datetime.strptime(end_date, formato_data)

    # Gera um número aleatório de dias entre as duas datas
    delta_tempo = data_fim - data_inicio
    dias_aleatorios = random.randint(0, delta_tempo.days)

    # Calcula a data aleatória adicionando os dias aleatórios à data de início
    data_aleatoria = data_inicio + timedelta(days=dias_aleatorios)

    # Retorna a data no formato desejado
    return data_aleatoria.strftime('%Y/%m/%d')


def generate_username(length: int = 8) -> str:
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_email() -> str:
    common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com',
                      'outlook.com', 'icloud.com']
    username = generate_username()
    domain = random.choice(common_domains)
    return f"{username}@{domain}"


def generate_CPF(num: int = 1):
    import random
    for i in range(0, num):

        def verificador_final(entrada):
            return 0 if ((entrada * 10) % 11) > 9 else ((entrada * 10) % 11)

        cpf = []
        cpf_str = []
        soma_primeiro_digito = 0
        soma_segundo_digito = 0
        _ = 0
        c1 = 10
        c2 = 11
        t = 0
        for i in range(0, 10):
            if t <= 8:
                _ = random.randint(0, 9)
                cpf.append(_)
                if t == 2:
                    cpf_str.append(str(_))
                    cpf_str.append('.')
                elif t == 5:
                    cpf_str.append(str(_))
                    cpf_str.append('.')
                elif t == 8:
                    cpf_str.append(str(_))
                    cpf_str.append('-')
                else:
                    cpf_str.append(str(_))
                soma_primeiro_digito += cpf[t] * c1
                soma_segundo_digito += cpf[t] * c2
                c1 -= 1
                c2 -= 1
            if t == 9:
                t += 3
                cpf_str.append(str(verificador_final(soma_primeiro_digito)))
                soma_segundo_digito += int(cpf_str[t]) * c2
                cpf_str.append(str(verificador_final(soma_segundo_digito)))
            t += 1
        cpf_gerado = ''

        for i in cpf_str:
            cpf_gerado += str(i)

        return cpf_gerado


# função usada para validar o cpf que o usuario digitar
#  e formatar para enviar no banco de dados
def validate_cpf(cpf: str) -> str | None:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return None
    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf_formatado


manage = SellerManagement()
opt = ""

while True:

    opt = input(
            "\n1 - Criar Base de dados e tabelas(arquivo: DataBase.db)\n"
            "2 - Inserir planilha de cadastro de vendedores\n"
            "3 - Criar ou atualizar o cadastro de um vendedor\n"
            "4 - Atualizar ou inserir tabela de vendas\n"
            "5 - Mostrar tabela de Vendedores\n"
            "6 - Mostrar tabela de Vendas\n"
            "7 - Mostrar tabela de Comissões\n"
            "8 - Deletar um vendedor no Banco de dados\n"
            "9 - Limpar uma tabela do Banco de dados\n"
            "10 - Calcular comissão da equipe\n"
            "11 - Mostrar quadro de vendas geral\n"
            "12 - Help (Em desenvolvimento) \n"
            "0 - Sair...\n"
            "Digite: "
            )

    match opt:

        # Essa opção cria as tabelas dentro do banco de dados ##
        case "1":
            manage.create_Sellers_Table()
            manage.create_Sales_Table()
            manage.create_Commission_Table()
            os.system("cls")
            print("Mensagem: Base de dados criando com sucesso!")

        # Essa opção atualiza os dados de cadastro dos vendedores no
        # banco de dados utilizando a planilha = Vendedores.xlsx##
        # Observação: A planilha Vendedores.xlsx deve estar na mesma
        # pasta deste script e conter o mesmo nome para funcionar)
        case "2":
            message = manage.data_Base_its_open()
            try:
                if message is None:
                    manage.clean_Table("Sellers")
                    manage.replace_Seller_Table()
                    os.system("cls")
                    print("Mensagem: Tabela De vendedores atualizado com sucesso")
                else:
                    print(message)
            except FileNotFoundError:
                print("Mensagem: Arquivo Vendedores.xlsx não encontrado")
            except Exception:
                print("Mensagem: Erro desconhecido ", Exception)

        # Essa opção altera informações diretamente no banco de dados ##
        case "3":
            message = manage.data_Base_its_open()
            if message is None:
                while True:
                    print(
                        "\n1 - Criar cadastro aleatório de vendedor\n"
                        "2 - Cadastro manual de vendedor\n"
                        "3 - Atualizar cadastro de vendedor\n"
                        "4 - Sair\n"
                        )
                    user = input("Digite: ")
                    match user:

                        # Essa opção gera um cadastro aleatorio para um vendedor
                        # ,apenas limitando pelo nome de vendedores que podem
                        # repetir pois criei uma lista Pequena, todas essas
                        # funções podem ser vistas acima no topo do codigo ##
                        case "1":
                            name = generate_name()
                            cpf = generate_CPF()
                            date_of_birth = generate_data()
                            email = generate_email()
                            state = generate_UF()
                            manage = SellerManagement(
                                name=name, cpf=cpf,
                                date_of_birth=date_of_birth,
                                email=email, state=state)
                            manage.update_Seller()
                            os.system("cls")
                            print("Mensagem: Cadastro registrado com sucesso")

                        # Essa opção, voce insere manualmente os dados de um vendedor #
                        case "2":
                            while True:

                                cpf = input("\nDigite o CPF ou 0 para encerrar: ")

                                # Essa função que vai tratar o cpf digitado
                                # para enviar da forma correta para o banco de dados
                                # Pode digitar tanto no formato "..-" ou sem ##
                                cpf_valid = validate_cpf(cpf)

                                # Essa função verifica se o cpf digitado existe
                                # no banco de dados
                                exist = manage.search(cpf_valid, "Sellers", "CPF")

                                if cpf == "0":
                                    break

                                elif exist is True:
                                    os.system("cls")
                                    print("Mensagem: CPF já cadastrado")

                                elif cpf_valid is None:
                                    os.system("cls")
                                    print("Mensagem: CPF invalido")

                                else:
                                    name = input("Nome: ")
                                    date_of_birth = input(
                                        "Data de nascimento no formato YYYY/MM/DD: "
                                    )
                                    email = input("Email: ")
                                    state = input("Estado(UF): ")
                                    manage = SellerManagement(
                                        name=name, cpf=cpf_valid,
                                        date_of_birth=date_of_birth,
                                        email=email, state=state)
                                    manage.update_Seller()
                                    os.system("cls")
                                    print("Mensagem: Cadastro registrado com sucesso")
                                    break

                        # Essa opção atualiza o cadastro de um vendedor no
                        # banco de dados utilizando cpf como parametro, apos uma
                        # validação de informaçoes, você insere manualmente cada
                        #  informação do vendedor
                        case "3":
                            while True:
                                cpf = input("\nDigite o CPF ou 0 para encerrar: ")

                                if cpf == "0":
                                    os.system("cls")
                                    break

                                # Pode digitar tanto no formato "..-" ou sem #
                                cpf_valid = validate_cpf(cpf)

                                exist = manage.search(cpf_valid, "Sellers", "CPF")

                                if exist is False:
                                    os.system("cls")
                                    print("Mensagem: CPF não encontrado")
                                    continue

                                else:
                                    name = input("Nome: ")
                                    date_of_birth = input("Data de nascimento no formato YYYY/MM/DD: ")
                                    email = input("Email: ")
                                    state = input("Estado(UF): ")
                                    manage = SellerManagement(
                                        name=name,
                                        cpf=cpf_valid,
                                        date_of_birth=date_of_birth,
                                        email=email, state=state)
                                    manage.update_Seller()
                                    os.system("cls")
                                    print("Mensagem: Cadastro atualizado com sucesso")
                                    break

                        # Essa opção apenas sai do laço atual para o laço anterior
                        case "4":
                            os.system("cls")
                            break

                        # Caso digite qualquer outra coisa, repetira esse laço
                        case _:
                            os.system("cls")
                            print("Mensagem: Opção incorreta!\n")

            # Esse trexo do codigo é o que da a mensagem de erro caso
            # as tabelas do banco de dados não forem criados
            else:
                os.system("cls")
                print(message)

        # Essa opção e onde voce insere a planilha = Vendas.xlsx no banco de dados
        case "4":
            message = manage.data_Base_its_open()
            if message is None:
                print(
                    "1 - Inserir na base de dados\n"
                    "2 - Atualizar a base de dados\n"
                    "3 - Sair\n"
                    )
                user = input("Digite: ")

                # Essa opção apenas insere as informaçãos, caso já tenha
                # informações no banco de dados ira incrementa-lo
                if user == "1":
                    manage.insert_Sales_Table()
                    os.system("cls")
                    print("Mensagem: Dados inseridos no banco de dados com sucesso.")

                # Essa opção atualiza completamente a tabela de vendas, ou seja,
                # apaga a tabela primeiro e depois insere  ##
                elif user == "2":
                    manage.clean_Table("Sales")
                    manage.insert_Sales_Table()
                    os.system("cls")
                    print("Mensagem: Banco de dados atualizado com sucesso.")

                # Sai do laço atual e volta para o menu
                elif user == "3":
                    os.system("cls")
                    continue

                # Caso digite qulquer outra coisa ira chegar aqui
                else:
                    os.system("cls")
                    print("Opção incorreta")

            # Caso não seja criado as tabelas no banco de dados,
            # ira mostrar uma memsagem de erro aqui
            else:
                os.system("cls")
                print(message)

        # Mostra no terminal a tabela de vendedores do banco de dados
        case "5":
            message = manage.data_Base_its_open()
            if message is None:
                os.system("cls")
                manage.read_Table("Sellers")
            else:
                print(message)

        # Mostra no terminal a tabela de vendas do banco de dados
        case "6":
            message = manage.data_Base_its_open()
            if message is None:
                os.system("cls")
                manage.read_Table("Sales")
            else:
                print(message)

        # Mostra no terminal a tabela de comissões do banco de dados
        case "7":
            message = manage.data_Base_its_open()
            if message is None:
                os.system("cls")
                manage.read_Table("Commission")
            else:
                print(message)

        # Essa opção voce consegue deletar um cadastro de um vendedor
        # inserindo o cpf
        case "8":
            message = manage.data_Base_its_open()
            if message is None:
                while True:

                    # Pode digitar tanto no formato "..-" ou sem
                    cpf = input("Digite o CPF ou 0 para sair: ")

                    if cpf == "0":
                        break

                    cpf_valid = validate_cpf(cpf)

                    if cpf_valid is None:
                        os.system("cls")
                        print("Mensagem: CPF invalido")

                    else:
                        exist = manage.search(cpf_valid, "Sellers", "CPF")

                        # Caso o manage.search encontre o CPF retornará True e
                        # em seguida o vendedor será deletado pelo delete_seller
                        if exist is True:
                            os.system("cls")
                            manage.delete_Seller(cpf_valid)
                            print("Mensagem: Colaborador removido com sucesso! ")
                            break

                        else:
                            os.system("cls")
                            print("Mensagem: Vendedor não localizado no banco de dados")
                            break
            else:
                print(message)

        # Essa opção limpa uma tabela a escolha
        case "9":
            message = manage.data_Base_its_open()
            if message is None:
                print(
                    "1 - Limpar tabela dos vendedores\n"
                    "2 - Limpar tabela das vendas\n"
                    "3 - Limpar tabela das comissão\n"
                    "4 - Sair\n"
                    )
                user = input("Digite: ")

                match user:
                    case "1":
                        manage.clean_Table("Sellers")
                        os.system("cls")
                        print("Mensagem: Todos os dados da tabela vendedores"
                              "foram apagados com sucesso!")
                    case "2":
                        manage.clean_Table("Sales")
                        os.system("cls")
                        print("Mensagem: Todos os dados da tabela foram vendas"
                              "apagados com sucesso!")
                    case "3":
                        manage.clean_Table("Commission")
                        os.system("cls")
                        print("Mensagem: Todos os dados da tabela commissôes"
                              "foram apagados com sucesso!")
                    case "4":
                        os.system("cls")
                        continue
                    case _:
                        os.system("cls")
                        print("Mensagem: Opção invalida")
            else:
                print(message)

        # Essa opção ira calcular a comissão dos vendedores utilizando toda as
        # vendas na tabela vendas do banco de dados
        case "10":
            message = manage.data_Base_its_open()
            if message is None:
                manage.clean_Table("Commission")
                manage.calculate_Commision()
                os.system("cls")
                print("Mensagem: Comissão gerado com sucesso!")
            else:
                print(message)

        # Essa opção mostra o quadro geral de vendas
        case "11":
            message = manage.data_Base_its_open()
            if message is None:
                os.system("cls")
                manage.show_General_Sales()
            else:
                print(message)

        case "12":
            os.system("cls")
            print(
                "1 - Help(main.py)\n"
                "2 - Help(ClassSeller.py)\n"
                "3 - Sair\n"
                )
            user = input("Digite: ")

            match user:
                case "1":
                    os.system("cls")
                    help()
                case "2":
                    os.system("cls")
                    help(ClassSeller)
                case "3":
                    os.system("cls")
                    continue
                case _:
                    os.system("cls")
                    print("Mensagem: Opção invalida")
            break

        case "0":
            os.system("cls")
            break
        case _:
            os.system("cls")
            print("Mensagem: Opção invalida")
