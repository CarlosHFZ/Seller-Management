
import pandas as pd
import sqlite3


class SellerManagement():
    def __init__(self, name=None, cpf=None, date_of_birth=None, email=None, state=None):
        self.name = name
        self.cpf = cpf
        self.date_of_birth = date_of_birth
        self.email = email
        self.state = state

# -------------- Funções para criação do banco de dados SQLite -------------- #

# Cria a tabela de Vendedores
    def create_Sellers_Table(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Sellers('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'Name TEXT,'
                       'CPF TEXT UNIQUE,'
                       'Date_of_birth TEXT,'
                       'Email TEXT,'
                       'State TEXT'
                       ')')
        
        cursor.close()
        connection.close()

## Cria a tabela de Vendas ##
    def create_Sales_Table(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Sales('
                       'id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,' 
                       'Date_of_Sale TEXT,'                      
                       'Sallers_name TEXT,'                       
                       'Sale FLOAT,'                       
                       'Client_type TEXT,'                       
                       'Sales_channel TEXT,'                       
                       'Cost_of_sale FLOAT'                       
                       ')')
        
        cursor.close()
        connection.close()

## Cria a tabela de Comissôes
    def create_Commission_Table(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Commission(' 
                       'Date_of_Payment TEXT,'                      
                       'Sallers_name TEXT UNIQUE,'                       
                       'Commission FLOAT'                                           
                       ')')
        
        cursor.close()
        connection.close()


##------------ Funções para ler as tabelas do banco de dados SQLite -------------##


## Mostra as informaçoes da tabela deseja inserindo o nome da tabela pelo main ##
    def read_Table(self, table_name):

        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()

        cursor.execute(f'SELECT * FROM {table_name}')
        
        collums = [description[0] for description in cursor.description]
        
        data = cursor.fetchall()
        
        print(f"{' | '.join(collums)}")
        print('-' * 40)

        for row in data:
            print(f"{' | '.join(map(str, row))}")
    
        cursor.close()
        connection.close()

## Mostra um quadro de vendas com total de vendas por regiao, vendedor, canal. ##
## Alem de mostra media da venda de um vendedor ##
    def show_General_Sales(self):
    # Conectando ao banco de dados
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()

        # Consulta para obter o volume de vendas e média de vendas por canal e estado
        query_general = """
        SELECT s.State, sa.Sales_channel, sa.Sallers_name, SUM(sa.Sale) AS Total_Sales, AVG(sa.Sale) AS Average_Sale_Per_Professional
        FROM Sales sa
        JOIN Sellers s ON sa.Sallers_name = s.Name
        GROUP BY s.State, sa.Sales_channel, sa.Sallers_name
        ORDER BY s.State, sa.Sales_channel, sa.Sallers_name
        """
        
        # Consulta para obter o total de vendas por região (estado)
        query_total_by_region = """
        SELECT s.State, SUM(sa.Sale) AS Total_Sales
        FROM Sales sa
        JOIN Sellers s ON sa.Sallers_name = s.Name
        GROUP BY s.State
        ORDER BY s.State
        """

        # Consulta para obter o total de vendas por canal
        query_total_by_channel = """
        SELECT sa.Sales_channel, SUM(sa.Sale) AS Total_Sales
        FROM Sales sa
        GROUP BY sa.Sales_channel
        ORDER BY sa.Sales_channel
        """

        # Executando as consultas
        cursor.execute(query_general)
        results_general = cursor.fetchall()

        cursor.execute(query_total_by_region)
        results_total_by_region = cursor.fetchall()

        cursor.execute(query_total_by_channel)
        results_total_by_channel = cursor.fetchall()
        
        # Exibindo os resultados gerais por canal, estado e vendedor
        print(f"{'State':<10} {'Channel':<20} {'Seller':<20} {'Total Sales (R$)':<20} {'Average Sale/Professional (R$)':<30}")
        print('-' * 100)
        for row in results_general:
            state, channel, seller, total_sales, avg_sale = row
            print(f"{state:<10} {channel:<20} {seller:<20} {total_sales:<20.2f} {avg_sale:<30.2f}")
        
        # Exibindo os resultados totais por região
        print("\nTotal de Vendas por Região (Estado)")
        print(f"{'State':<10} {'Total Sales (R$)':<20}")
        print('-' * 30)
        for row in results_total_by_region:
            state, total_sales = row
            print(f"{state:<10} {total_sales:<20.2f}")
        
        # Exibindo os resultados totais por canal
        print("\nTotal de Vendas por Canal")
        print(f"{'Channel':<20} {'Total Sales (R$)':<20}")
        print('-' * 40)
        for row in results_total_by_channel:
            channel, total_sales = row
            print(f"{channel:<20} {total_sales:<20.2f}")
        cursor.close()
        connection.close()

##----------- Funções para atualizar o banco de dados SQlite --------------##


## Adciona ou atualiza os dados de um Vendedor quando inserido nos atributos da classe no main ##
## Alem disso essa função verifica se já existe um cpf cadastrado, se sim aplica um UPDATE para atualizar as informalçioes, se não aplica um INSERT para adicionar##
    def update_Seller(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * from Sellers")

        
        cursor.execute("INSERT INTO Sellers(Name, CPF, Date_of_birth, Email, State)"
                    "VALUES (?, ?, ?, ?, ?) ON CONFLICT(CPF) DO UPDATE SET "
                    "Name = excluded.Name, Date_of_birth = excluded.Date_of_birth, "
                    "Email = excluded.Email, State = excluded.State",
                    (self.name, self.cpf, self.date_of_birth, self.email, self.state))
        connection.commit()
        cursor.close()
        connection.close()       

## Substitui os dados da tabela Sallers pela planilha Exccel Vendedores.xlsx ##
    def replace_Seller_Table(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        table = pd.read_excel("Vendedores.xlsx") 
    
        for index, row in table.iterrows():
            date_str = pd.to_datetime(row.iloc[2], format="%d/%m/%y").strftime("%Y/%m/%d")

            cursor.execute("INSERT INTO Sellers(Name, CPF, Date_of_birth, Email, State)"
                        "VALUES (?, ?, ?, ?, ?) ON CONFLICT(CPF) DO UPDATE SET "
                        "Name = excluded.Name, Date_of_birth = excluded.Date_of_birth, "
                        "Email = excluded.Email, State = excluded.State",
                        (row.iloc[0], row.iloc[1], date_str, row.iloc[3], row.iloc[4]))
            connection.commit()
        cursor.close()
        connection.close()

## Insere os dados da planilha Vendas.xlsx no banco de dados SQLite ##
    def insert_Sales_Table(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        table_sales = pd.read_excel("Vendas.xlsx", sheet_name=0)       
        # table_payments = pd.read_excel("Vendas.xlsx", sheet_name=1) 
    
        for index, row in table_sales.iterrows():
            date_str = pd.to_datetime(row.iloc[0], format="%d/%m/%y").strftime("%Y/%m/%d")

            cursor.execute("INSERT INTO Sales(Date_of_Sale, Sallers_name, Sale, Client_type, Sales_channel, Cost_of_sale)"
                        "VALUES (?, ?, ?, ?, ?, ?)", (date_str, row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5],))
            connection.commit()
        cursor.close()
        connection.close()


    def clean_Table(self, table) -> str:
        """Função para limpar uma tabela

            Limpa os dados da tabela escolhida(Sellers, Sales ou Commission)

        """
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table}")
        connection.commit()    
        cursor.close()
        connection.close()  

## Deleta o cadastro de um vendedor no banco de dados pelo CPF ##
    def delete_Seller(self, cpf):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cpf_local = cpf
        cursor.execute("DELETE FROM Sellers WHERE CPF = ? ", (cpf_local,))
        connection.commit()

        row_affected = cursor.rowcount
        if row_affected == 0:
            cursor.close()
            connection.close()
            return None
        else:
            cursor.close()
            connection.close()
            return not None           


## Funcão para calcular as comissões usando a tabela Sales e tbm cria a tabela de comissão ##
    def calculate_Commision(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()      
        
        commision_base = 0.0
        commision_actually = 0.0
        marketing_comission = 0.0
        marketing_comission_total = 0.0
        manager_comission_total = 0.0

        cursor.execute("SELECT Sallers_name, Sale, Sales_channel FROM Sales")
        for seller in cursor.fetchall():
            Sale_value = seller[1]

            cursor.execute("SELECT Commission FROM Commission WHERE Sallers_name = ?", (seller[0],))            
            seller_comission = cursor.fetchone()
            if seller_comission is not None:
                commision_base = seller_comission[0]
                
            if isinstance(Sale_value, str):           
                Sale_value = Sale_value.replace('R$', '').replace('.', '').replace(',', '.').strip()
                Sale_value_float = float(Sale_value)
                commision_actually = Sale_value_float * 0.10 
            else:                 
                commision_actually = Sale_value * 0.10
            
            if seller[2] == "Online":
                marketing_comission_total += commision_actually * 0.20
                marketing_comission = commision_actually * 0.20
                commision_actually -= marketing_comission

            commision_base += commision_actually
           
            cursor.execute("INSERT INTO Commission(Date_of_Payment, Sallers_name, Commission)"
                        "VALUES (?, ?, ?) ON CONFLICT(Sallers_name) DO UPDATE SET "
                        "Date_of_Payment = excluded.Date_of_Payment,  Sallers_name = excluded.Sallers_name, "
                        "Commission = excluded.Commission",          
                        ("2024/06/19", seller[0], commision_base))
            commision_base = 0.0
            connection.commit()


        cursor.execute("SELECT Commission FROM Commission")
        for commission in cursor.fetchall():         
            if commission[0] >= 1000:
                manager_comission_total += commission[0] * 0.10


        cursor.execute("INSERT INTO Commission(Date_of_Payment, Sallers_name, Commission)"
                    "VALUES (?, ?, ?) ON CONFLICT(Sallers_name) DO UPDATE SET "
                    "Date_of_Payment = excluded.Date_of_Payment,  Sallers_name = excluded.Sallers_name, "
                    "Commission = excluded.Commission",          
                    ("2024/06/19", "Gerente De Vendas", manager_comission_total))
        connection.commit()
            
        cursor.execute("INSERT INTO Commission(Date_of_Payment, Sallers_name, Commission)"
                    "VALUES (?, ?, ?) ON CONFLICT(Sallers_name) DO UPDATE SET "
                    "Date_of_Payment = excluded.Date_of_Payment,  Sallers_name = excluded.Sallers_name, "
                    "Commission = excluded.Commission",          
                    ("2024/06/19", "Marketing", marketing_comission_total))
        connection.commit()
                      
        cursor.close()
        connection.close()

## Fiz essa função somente para verificar se as tabelas do banco de dados foram criadas ##
## retorna None caso as tabelas foram criadas corretamente ou uma mensagem de erro caso não ##
    def data_Base_its_open(self):
                import os
                os.system("cls")
                try:                   
                    connection = sqlite3.connect("DataBase.db")
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Sellers")
                    cursor.execute("SELECT * FROM Sales")
                    cursor.execute("SELECT * FROM Commission")
                    cursor.close
                    connection.close()
                    return None
                except sqlite3.OperationalError:
                    cursor.close
                    connection.close()
                    os.system("cls")
                    return "Mensagem: O banco de dados não foi criado!",
                except Exception:
                    cursor.close
                    connection.close()
                    os.system("cls")
                    return f"Mensagem: Erro desconhecido! --->",Exception

## Fiz essa função apenas para buscar uma informação especifca no banco de dados ##                
    def search(self, data, table, where):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()

        cursor.execute(f" SELECT COUNT(*) FROM {table} WHERE {where} = ? ", (data,))
        resultado = cursor.fetchone()

        connection.close()

        return resultado[0] > 0
    





                            