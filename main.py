from ClassSeller import SellerManagement
import os
import random
import string
from datetime import datetime, timedelta
import sqlite3


def generate_name():
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'William', 'Jessica', 'David', 'Emily', 'Robert', 'Linda']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_UF():
    first_letter = ['S', 'S', 'G', 'M', 'B',]
    second_letter = ['C', 'P', 'O', 'G', 'A',]
    one = random.choice(first_letter)
    two = random.choice(second_letter)
    return f"{one}{two}"

def generate_data(start_date='1925-01-01', end_date='2020-12-31'):
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

def generate_username(length=8):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_email():
    common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com']
    username = generate_username()
    domain = random.choice(common_domains)
    return f"{username}@{domain}"

def generate_CPF(num=1):
    for i in range(0, num):
        import random

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
            cpf_gerado += i
        return cpf_gerado

def validate_cpf(cpf: str) -> str:

    cpf = ''.join(filter(str.isdigit, cpf))

 
    if len(cpf) != 11:
        return None

    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return cpf_formatado


manage = SellerManagement()
opt = -1

while (opt != 0):

    opt = input(
            "\n\n1 - Criar Base de dados e tabelas(arquivo: DataBase.db)\n"
            "2 - Inserir planilha de cadastro de vendedores(deve estar na mesma pasta deste script)\n"
            "3 - Criar ou atualizar o cadastro de um vendedor\n"
            "4 - Atualizar ou inserir tabela de vendas\n"
            "5 - Mostrar tabela de Vendedores\n"
            "6 - Mostrar tabela de Vendas\n"
            "7 - Mostrar tabela de Comissões\n"
            "8 - Deletar um vendedor no Banco de dados\n"
            "9 - limpar uma tabela do Banco de dados\n"
            "10 - Calcular comissao da equipe\n"
            "11 - Mostrar quadro de vendas geral\n"
            "0 - Sair...\n"
            "Digite: "
            )

    
    match opt:
        case "1":
            manage.create_Sellers_Table()
            manage.create_Sales_Table()
            manage.create_Commission_Table()
            os.system("cls")
            print("Mensagem: Base de dados criando com sucesso!")

        case "2":
            message = manage.data_Base_its_open() 
            if message is None:
                manage.replace_Seller_Table()
                os.system("cls")
                print("Mensagem: Tabela De vendedores atualizado com sucesso")
            else:
                print(message)
        case "3":
            message = manage.data_Base_its_open()  
            if message is None:
                print("1 - Criar cadastro aleatório\n"
                    "2 - Cadastro manual\n"
                    "3 - Sair\n"
                    )
                user = input("Digite: ")
                if user == "1":
                    name = generate_name()
                    cpf = generate_CPF()
                    date_of_birth = generate_data()     
                    email = generate_email()
                    state = generate_UF()
                    manage = SellerManagement(name=name, cpf=cpf, date_of_birth=date_of_birth, email=email, state=state)
                    manage.update_Seller()
                    os.system("cls")
                    print("Mensagem: Cadastro registrado com sucesso")

                elif user == "2":
                    name = input("Nome: ")
                    while True:
                        cpf = input("Digite o CPF ou 0 para encerrar: ")
                        cpf_valid = validate_cpf(cpf)
                        if cpf == "0":
                            break

                        elif cpf_valid is None:
                            os.system("cls")
                            print("Mensagem: CPF invalido")


                        else:
                            date_of_birth = input("Data de nascimento no formato YYYY/MM/DD: ")    
                            email = input("Email: ")
                            state = input("Estado(UF): ")
                            manage = SellerManagement(name=name, cpf=cpf_valid, date_of_birth=date_of_birth, email=email, state=state)
                            manage.update_Seller()
                            os.system("cls")
                            print("Mensagem: Cadastro registrado com sucesso")
                            break
                elif user == "3":
                    continue
                else:
                    print("Opção incorreta")
            else:
                print(message)


        case "4":
            message = manage.data_Base_its_open()  
            if message is None: 
                print("1 - Inserir na base de dados\n"
                    "2 - Atualizar a base de dados\n"
                    "3 - Sair\n"
                    )
                user = input("Digite: ")
                if user == "1":
                    manage.insert_Sales_Table()
                    os.system("cls")
                    print("Mensagem: Dados inseridos no banco de dados com sucesso.")
                elif user == "2":
                    manage.clean_Table("Sales")
                    manage.insert_Sales_Table()
                    os.system("cls")
                    print("Mensagem: Banco de dados atualizado com sucesso.")
                elif user == "3":
                    os.system("cls")
                    continue
                else:
                    os.system("cls")
                    print("Opção incorreta")
            else:
                print(message)

        case "5":
            message = manage.data_Base_its_open()  
            if message is None:
                os.system("cls")
                manage.read_Table("Sellers")
            else:
                print(message)

        case "6":
            message = manage.data_Base_its_open()  
            if message is None:
                os.system("cls")
                manage.read_Table("Sales")
            else:
                print(message)

        case "7":
            message = manage.data_Base_its_open()  
            if message is None:
                os.system("cls")
                manage.read_Table("Commission")
            else:
                print(message)

        case "8":
            message = manage.data_Base_its_open()  
            if message is None:
                while True:
                    cpf = input("Digite o CPF: ")
                    validation = validate_cpf(cpf)
                    if validation is None:
                        os.system("cls")
                        print("Mensagem: CPF invalido")
                        break
                    else:
                        validation_2 = manage.delete_Seller(validation)
                        if validation_2 is None:
                            os.system("cls")
                            print("Mensagem: Vendedor não localizado no banco de dados")
                            break
                        else:
                            os.system("cls")
                            print("Mensagem: Colaborador removido com sucesso! ")
                            break
            else:
                print(message)

        case "9":
            message = manage.data_Base_its_open()  
            if message is None:
                print("1 - Limpar tabela dos vendedores\n"
                    "2 - Limpar tabela das vendas\n"
                    "3 - Limpar tabela das comissão\n"
                    "4 - Sair\n"
                    )
                user = input("Digite: ")
                match user:
                    case "1":
                        manage.clean_Table("Sellers")
                        os.system("cls")
                        print("Mensagem: Todos os dados da tabela foram apagados com sucesso!")
                    case "2":
                        manage.clean_Table("Sales")
                        os.system("cls")
                        print("Mensagem: Todos os dados da tabela foram apagados com sucesso!")
                    case "3":
                        manage.clean_Table("Commission")
                        os.system("cls")
                        print("Mensagem: Todos os dados da tabela foram apagados com sucesso!")
                    case "4":
                        os.system("cls")
                        continue
                    case _:
                        os.system("cls")
                        print("Mensagem: Opção invalida")
            else:
                print(message)
           
        case "10":
            message = manage.data_Base_its_open()  
            if message is None:
                manage.clean_Table("Commission")
                manage.calculate_Commision()
                os.system("cls")
                print("Mensagem: Comissão gerado com sucesso!")
            else:
                print(message)

        case "11":
            message = manage.data_Base_its_open()  
            if message is None:
                os.system("cls")
                manage.show_General_Sales()
            else:
                print(message)

        case "0":
            os.system("cls")
            print("Saindo...")
            break


        case _:
            os.system("cls")
            print("Mensagem: Opção invalida")    
        
