from ClassSeller import SellerManagement



print("insert to data base")
seller = SellerManagement("Carlos Henrique",
                          "127.759.639-01",
                          "17/01/2001",
                          "carlintos@hotmail.com",
                          "PA")

seller.create_Sellers_Database()
seller.create_Sales_Database()

# Nome do Vendedor	CPF	Data De Nascimento	Email	Estado
# João Silva	806.022.515-40	17/01/2001	joao@outlook.com	SC
# Maria Oliveira	193.347.010-05	18/11/2003	maria@gmail.com	SP
# Pedro Souza	269.969.930-67	19/02/1998	pedro@hotmail.com	SC
# Ana Costa	475.120.632-02	02/09/1983	ana@outlook.com.br	SC
# Carlos Santos	428.398.462-09	18/11/2003	carlos@hotmail.com.br	GO
# Daniella Fernandes	084.245.147-18	22/04/1995	daniela@outlook.com	GO


