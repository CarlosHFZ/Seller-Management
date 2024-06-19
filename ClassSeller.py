
import pandas as pd
import sqlite3


class SellerManagement():
    def __init__(self, name=None, cpf=None, date_of_birth=None, email=None, state=None):
        self.name = name
        self.cpf = cpf
        self.date_of_birth = date_of_birth
        self.email = email
        self.state = state

    def create_Sellers_Database(self):
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

    def create_Sales_Database(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Sales('
                       'Date_of_Sale TEXT,'                      
                       'Sallers_name TEX,'                       
                       'Sale FLOAT,'                       
                       'Client type TEXT,'                       
                       'Sales_channel TEXT,'                       
                       'Cost_of_sale FLOAT'                       
                       ')')
        
        cursor.close()
        connection.close()


    def read(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sellers")
        collums =  [description[0] for description in cursor.description]
        print(f"|  {collums[0]}  |       {collums[1]}      |     {collums[2]}       |  {collums[3]}  |      {collums[4]}               | {collums[5]} |")
        c = 0
        for row in cursor.fetchall():
            print("  ",end="")
            for value in row:
                print(f"{value}",end="     ")
    
    

        cursor.close()
        connection.close()
    
    def update_Seller(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        # cpf_data_base = []
        cursor.execute("SELECT * from Sellers")
        # for i in cursor:
        #     cpf_data_base.append(i[2])
        # if self.cpf in cpf_data_base:
        #     cursor.execute("UPDATE Sellers SET Name = ?, Date_of_birth = ?, Email = ?, State = ? WHERE CPF = ?",
        #                    (self.name, self.date_of_birth, self.email, self.state, self.cpf))
        #     connection.commit()
        #     cursor.close()
        #     connection.close()
        #     return "Cadastro De vendedor Atualizado"
        # else:
        #     cursor.execute("INSERT INTO Sellers(Name, CPF, Date_of_birth, Email, State)"
        #                 "VALUES (?, ?, ?, ?, ?)", 
        #                 (self.name, self.cpf, self.date_of_birth, self.email, self.state))
        #     connection.commit()
        #     cursor.close()
        #     connection.close()
        #     return "Vendedor Cadastrado"
        
        cursor.execute("INSERT INTO Sellers(Name, CPF, Date_of_birth, Email, State)"
                    "VALUES (?, ?, ?, ?, ?) ON CONFLICT(CPF) DO UPDATE SET "
                    "Name = excluded.Name, Date_of_birth = excluded.Date_of_birth, "
                    "Email = excluded.Email, State = excluded.State",
                    (self.name, self.cpf, self.date_of_birth, self.email, self.state))
        connection.commit()
        cursor.close()
        connection.close()       

    def delete_dataBase(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Sellers")
        connection.commit()    
        cursor.close()
        connection.close()  

    def delete_Seller(self, cpf):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Sellers WHERE CPF = ? ", (cpf,))
        connection.commit()    
        cursor.close()
        connection.close()           

    def replace_DataBase(self):
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
    
    def replace_Sales_DataBase(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        table = pd.read_excel("Sales.xlsx") 
    
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

    def calc_Commision(self):       
        table = pd.read_excel("Vendas.xlsx")



    
