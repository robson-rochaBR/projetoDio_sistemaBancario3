# projetoDio_sistemaBancario3
Este é um sistema bancário simples, desenvolvido em Python, que simula operações financeiras básicas como depósito, saque e extrato. O projeto foi criado com foco na aplicação de conceitos de Programação Orientada a Objetos (POO), como herança, polimorfismo, encapsulamento e abstração.

## 🚀 Funcionalidades
### O sistema oferece as seguintes funcionalidades por meio de um menu interativo:

Depósito: Adiciona um valor à conta do cliente.

Saque: Retira um valor da conta, respeitando o limite e o número de saques diários.

Extrato: Exibe o histórico de transações e o saldo atual da conta.

Novo Cliente: Permite o cadastro de um novo cliente (Pessoa Física).

Criar Conta: Cria uma nova conta corrente para um cliente existente.

Listar Contas: Exibe todas as contas cadastradas no sistema.

## 🧠 Arquitetura do Projeto
### O código é estruturado em classes para representar entidades do mundo real, como:

Cliente e PessoaFisica: Gerenciam os dados dos clientes e suas contas.

Conta e ContaCorrente: Controlam as operações de saldo, saques e depósitos, com a ContaCorrente herdando e expandindo as funcionalidades da classe base.

Transacao (Abstrata), Saque e Deposito: Implementam o padrão de design Strategy, permitindo que as transações sejam registradas de forma uniforme.

Historico: Armazena e gerencia todas as transações de uma conta.

A lógica de negócios e as interações com o usuário são separadas para garantir um código mais limpo e modular.

## ✍️ Melhorias Futuras
O projeto pode ser expandido com as seguintes melhorias:

Validação de Entrada: Adicionar validações mais robustas para entradas do usuário (ex: CPF, datas, valores).

Múltiplas Contas por Cliente: Permitir que um cliente tenha mais de uma conta.

Interface Gráfica: Desenvolver uma interface gráfica para o usuário em vez do terminal.

Persistência de Dados: Salvar as informações de clientes e contas em um arquivo (como JSON ou CSV) para que os dados não sejam perdidos ao encerrar o programa.

### Autor
[Robson Rocha] - [www.linkedin.com/in/robsonoliveirarocha]


