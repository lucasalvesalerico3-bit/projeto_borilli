from banco_de_dados import (
    criar_tabelas,
    cadastrar_funcionario,
    listar_funcionarios,
    excluir_funcionario,
    atualizar_funcionario,
    cadastrar_metas,
    listar_metas,
    excluir_metas,
    atualizar_metas,
    apontar_realizado,
)

criar_tabelas()

while True:
    print("\n==========SISTEMA DE METAS==========")
    print("1- Cadastrar Funcionários: ")
    print("2 - Listar Funcionários: ")
    print("3 - Excluir Funcionários: ")
    print("4 - Atualizar Funcionários: ")
    print("5 - Cadastrar Metas: ")
    print("6 - Listar Metas: ")
    print("7 - Excluir Metas: ")
    print("8 - Atualizar Metas: ")
    print("9 - Apontar quantidade realizada: ")
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

    elif opcao == "4":
        nome = input("Digite o nome do funcionário a ser alterado:")
        cargo = input("Digite seu novo cargo: ")
        funcionario_id = int(input(" Digite a ID a ser alterada: "))
        atualizar_funcionario(nome, cargo, funcionario_id)

        print("Funcionário Atualizado com sucesso!")

    elif opcao == "5":
        funcionario_id = input("Digite a ID do Funcionário: ")
        data = input("Digite a data de hoje: ")
        meta = int(input("Digite a meta para o dia de hoje: "))
        cadastrar_metas(funcionario_id, data, meta)

        print("Meta Cadastrada com sucesso!")

    elif opcao == "6":

        listar_metas()

    elif opcao == "7":

        funcionario_id = int(input("Digite a ID do funcionário que deseja excluir a meta: "))
        excluir_metas(funcionario_id)

        print("Meta Excluida com sucesso!")

    elif opcao == "8":

        listar_metas()

        meta_id = int(input("Digite a ID da meta que deseja alterar: "))
        funcionario_id = int(input("Digite a ID do funcionário: "))
        data = input("Digite a nova data (AAAA-MM-DD): ")
        meta = float(input("Digite a nova meta: "))
        atualizar_metas(meta_id, funcionario_id, data, meta)

        print("Meta atualizada com sucesso!")

    elif opcao == "9":

       listar_metas()

       meta_id = int(input("Digite a ID da meta que deseja apontar o realizado: "))
       realizado = int(input("Digite a quantidade realizada: "))

       apontar_realizado(meta_id, realizado)

       print("Quantidade realizada cadastrada com sucesso!")

    elif opcao == "0":
        print("Encerrando o Sistema.")
        break

    else:
        print("Opção inválida!")
