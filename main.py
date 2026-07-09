from banco_de_dados import criar_tabelas, cadastrar_funcionario, listar_funcionarios

criar_tabelas()
listar_funcionarios()

print("==========SISTEMA DE METAS==========")

nome = input("Funcionário:")
cargo = input("Cargo:")

cadastrar_funcionario(nome, cargo)

print("Funcionário cadastrado com sucesso!")