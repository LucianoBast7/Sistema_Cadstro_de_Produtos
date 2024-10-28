# Sistema de Controle de Estoque

Este projeto é um sistema de controle de estoque desenvolvido em Python, utilizando SQLite para gerenciamento de dados e Tkinter para a interface gráfica. O sistema permite o gerenciamento de produtos e usuários, com funcionalidades para cadastro, visualização e atualização de informações.

## Funcionalidades

### Gerenciamento de Produtos
- **Cadastrar Produto:** Permite o cadastro de novos produtos com informações como nome, quantidade, quantidade mínima e descrição.
- **Visualizar Estoque:** Exibe todos os produtos cadastrados no estoque em uma tabela.
- **Atualizar Produto:** Permite atualizar a quantidade de um produto existente.
- **Excluir Produto:** Permite a exclusão de um produto do estoque.
- **Alertas de Estoque:** Notifica quando produtos estão abaixo da quantidade mínima definida.

### Gerenciamento de Usuários
- **Cadastrar Usuário:** Permite o cadastro de novos usuários com nome de usuário, senha e perfil (Administrador ou Comum).
- **Login de Usuário:** Implementa um sistema de login para acessar as funcionalidades do sistema.

### Gerenciamento de Movimentações
- **Registrar Movimentação:** Permite registrar entradas e saídas de produtos, atualizando as quantidades no estoque.
- **Visualizar Movimentações:** Exibe todas as movimentações realizadas, permitindo o acompanhamento do histórico de entradas e saídas.

## Estrutura do Banco de Dados

O banco de dados SQLite contém três tabelas principais:

### Tabela `produtos`
| Coluna             | Tipo    | Descrição                                   |
|--------------------|---------|---------------------------------------------|
| id_produto         | INTEGER | Identificador único do produto (chave primária) |
| nome               | TEXT    | Nome do produto                             |
| quantidade         | INTEGER | Quantidade disponível do produto            |
| quantidade_minima  | INTEGER | Quantidade mínima do produto                |
| descricao          | TEXT    | Descrição do produto                        |

### Tabela `usuarios`
| Coluna             | Tipo    | Descrição                                   |
|--------------------|---------|---------------------------------------------|
| id_usuario         | INTEGER | Identificador único do usuário (chave primária) |
| nome_usuario       | TEXT    | Nome de usuário (único)                    |
| senha              | TEXT    | Senha do usuário                            |
| perfil             | TEXT    | Perfil do usuário (Administrador ou Comum) |

### Tabela `movimentacoes`
| Coluna              | Tipo    | Descrição                                   |
|---------------------|---------|---------------------------------------------|
| id_movimentacao     | INTEGER | Identificador único da movimentação (chave primária) |
| id_produto          | INTEGER | Identificador do produto (chave estrangeira) |
| tipo_movimentacao   | TEXT    | Tipo da movimentação (entrada ou saída)    |
| quantidade          | INTEGER | Quantidade movimentada                      |
| data                | TEXT    | Data e hora da movimentação                 |
| descricao           | TEXT    | Descrição adicional da movimentação         |

#### Exemplos de Uso da Tabela `movimentacoes`

1. **Registrar Entrada:** Quando um novo lote de produtos chega, o usuário pode registrar uma entrada, especificando o produto, a quantidade recebida e uma descrição.
2. **Registrar Saída:** Quando produtos são vendidos ou retirados do estoque, o usuário pode registrar uma saída, informando a quantidade e o motivo.

