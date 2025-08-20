from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# Classe 01
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe 02
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print('\n### Desculpe! Saldo insuficiente. ###')
        
        elif valor > 0:
            self._saldo -= valor
            print('\n=== Saque realizado com sucesso! ===')
            return True
        else:
            print('\n### Operação falhou! O valor informado é inválido. ###')
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===')
            return True
        else:
            print('\n### Desculpe! Valor de depósito inválido. ###')
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print('### Operação falhou! O valor do saque excedeu o limite. ###')
        elif excedeu_saques:
            print('### Operação falhou! Numero maximo de saques excedido. ###')
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agência: {self.agencia}
            C/c: {self.numero}
            Titular: {self.cliente.nome}"""

# Classe 03
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            }
        )

# Classe 04
class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    menu_str = """
Banco do Brasil SA.
============= Menu =============
[1] - Depósito
[2] - Saque
[3] - Extrato
[4] - Novo Cliente
[5] - Criar conta
[6] - Listar contas
[0] - Sair
================================
▶ """
    try:
        return int(input(textwrap.dedent(menu_str)))
    except ValueError:
        return -1 # Retorna um valor inválido para o loop

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None
    
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('### Cliente não possui conta! ###')
        return
    return cliente.contas[0]
    
# Função auxiliar
def _recuperar_conta_para_transacao(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("### Cliente não encontrado! ###")
        return None
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return None

    return conta

def depositar(clientes):
    conta = _recuperar_conta_para_transacao(clientes)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor para deposito: "))
    except ValueError:
        print("\n### Valor inválido! Por favor, insira um número. ###")
        return

    transacao = Deposito(valor)
    conta.cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    conta = _recuperar_conta_para_transacao(clientes)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor para saque: "))
    except ValueError:
        print("\n### Valor inválido! Por favor, insira um número. ###")
        return

    transacao = Saque(valor)
    conta.cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("### Cliente não encontrado! ###")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================== EXTRATO ==================")
    transacoes = conta.historico.transacoes
    extrato = ""
    
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}\n"
    
    print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}")
    print("=============================================")

def criar_cliente(clientes):    
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("### Cliente já cadastrado com esse CPF! ###")  
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/estado): ")    

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário para quem a conta será criada: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n### Cliente não encontrado! Crie o usuário primeiro. ###")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")
        
def listar_contas(contas):
    if not contas:
        print("\n### Não há contas cadastradas. ###")
        return
        
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
        
def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        print()

        if opcao == 1:
            depositar(clientes)
        
        elif opcao == 2:
            sacar(clientes)
        
        elif opcao == 3:
            exibir_extrato(clientes)
        
        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 6:
            listar_contas(contas)
        
        elif opcao == 0:
            print("Obrigado por utilizar nossos serviços!")
            break
        
        else:
            print('\n### Opção inválida! Por favor, escolha uma opção válida. ###')


main()