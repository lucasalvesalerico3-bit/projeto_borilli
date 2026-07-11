from banco_de_dados import (
    criar_tabelas,
    cadastrar_funcionario,
    listar_funcionarios,
    excluir_funcionario
)

criar_tabelas()

while True:
    print("\n==========SISTEMA DE METAS==========")
    print("1- Castrar Funcionários: ")
    print("2 - Listar Funcionários: ")
    print("3 - Excluir Funcionários: ")
    print("0 - Encerrar o Sistema: ")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        nome = input("Funcionário: ")
        cargo = input("Cargo: ")
        cadastrar_funcionario(nome, cargo)

        print("Funcionário Cadastrado: ")

    elif opcao == "2":

        listar_funcionarios()

    elif opcao == "3":

        funcionario_id = int(input(" Digite a ID: "))
        excluir_funcionario(funcionario_id)

        print("Funcionário excluído! ")

    elif opcao == "0":
        print("Encerrando o Sistema:")
        break

    else:
        print("Opção inválida!")
