# Seller Management

Este programa foi desenvolvido para para gerenciar dados de vendedores e vendas. Eis o que ele oferece:

## Banco de Dados:
- Criação de um banco de dados.
- Criação de tabelas no banco de dados.

## Integração com Planilhas Excel:
- Importa informações de vendas e cadastros de vendedores em planilhas Excel para o banco de dados.

## Cadastro de Vendedores:
- Criação, atualização e exclusão de registros de vendedores.

## Visualização de Dados:
- Exibe tabelas diretamente no terminal.
- Apresenta um resumo geral de vendas por setor, região e canal.

## Limpeza de Dados:
- Limpa tabelas específicas ou todas as tabelas do banco de dados.

## Cálculo de Comissões:
- Calcula comissões para vendedores, marketing e gerentes de vendas.

## Testes Automatizados:
- Inclui testes para garantir a integridade dos dados.

A exibição ocorre no terminal Python e utilizei o DB Browser (SQLite) para acompanhar as movimentações de dados. 
Meu programa é desenvolvido em Python, faz uso do SQLite3 e utiliza a biblioteca Pandas. .

## Casos de Uso

1. Crie uma classe para gerenciar vendedores (todas as funções de um CRUD - Create, Read, Update e Delete).
  - Considere pelo menos os seguintes atributos: Nome, CPF, data de nascimento, e-mail e estado (UF).

2. Uma função para realizar a leitura de uma planilha com dados dos vendedores para adicionar ou atualizar em lote.
   
  - Considere o CPF como chave para a atualização.

3. Uma função para realizar a leitura de uma planilha de vendas (ex: https://docs.google.com/spreadsheets/d/1F8KUo66P5pQ1MKTPxU39li5S75rhATSy4C5EMNcJNOc/edit?usp=sharing) e calcular as comissões que devem ser pagas para cada vendedor. Considere as seguintes regras para as comissões:
   
  - Cada vendedor recebe 10% do valor de cada venda como comissão. 
  - Se a venda foi realizada por um canal online, 20% da comissão destinada ao vendedor é direcionada para a equipe de marketing.
  - Se o valor total das comissões do vendedor for maior ou igual a R$ 1.000,00, 10% da comissão é destinada ao gerente de vendas.

4. Apresentar o volume de vendas (R$) e média por profissional para cada canal e por cada estado.

5. [BÔNUS] Utilize um banco de dados para armazenar os dados (ex: postgresql ou sqlite).

6. [BÔNUS] Escreva testes para as classes e funções criadas.

