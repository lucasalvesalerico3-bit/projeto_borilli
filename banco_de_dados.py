# importando o SQLite3
import sqlite3

#criando a função para conectar ao banco de dados
def conectar():
    return sqlite3.connect("metas.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metas ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER, 
    mes TEXT,
    meta REAL,
    realizado  REAL DEFAULT 0, 
    FOREIGN KEY (funcionarios_id)
    REFERENCES funcionarios(id)
    )
    """)

def cadastrar_funcionario(nome, cargo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO funcionarios (nome, cargo) VALUES (?, ?)",
        (nome, cargo)
    )

    conn.commit()

def listar_funcionarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM funcionarios")

    funcionarios = cursor.fetchall()

    for funcionarios in funcionarios:
        print(funcionarios)

    conn.commit()
    conn.close()
