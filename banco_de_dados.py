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
    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metas ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER, 
    data TEXT,
    meta REAL,
    realizado  REAL DEFAULT 0, 
    FOREIGN KEY (funcionario_id)
    REFERENCES funcionarios(id)
    )
    """)
    conn.commit()
    conn.close()

def cadastrar_funcionario(nome, cargo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO funcionarios (nome, cargo) VALUES (?, ?)",
        (nome, cargo)
    )

    conn.commit()
    conn.close()

def listar_funcionarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM funcionarios")

    funcionarios = cursor.fetchall()

    for funcionarios in funcionarios:
        print(funcionarios)

def excluir_funcionario(funcionario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM funcionarios WHERE id = ?",
        (funcionario_id,)
    )
    conn.commit()
    conn.close()

def atualizar_funcionario(nome, cargo, funcionario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE funcionarios SET nome = ?, cargo = ? WHERE id = ?",
        (nome, cargo, funcionario_id)
    )
    conn.commit()
    conn.close()

def cadastrar_metas(funcionario_id, data, meta):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO metas (funcionario_id, data, meta) VALUES (?, ?, ?)",
        (funcionario_id, data, meta)
    )
    conn.commit()
    conn.close()

def listar_metas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        metas.id,
        funcionarios.nome,
        metas.data,
        metas.meta,
        metas.realizado
    FROM metas
    JOIN funcionarios
    ON metas.funcionario_id = funcionarios.id"""
    )
    resultado = cursor.fetchall()

    for linha in resultado:
        print(linha)

    conn.close()

def excluir_metas(funcionario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM metas WHERE funcionario_id = ?",
        (funcionario_id,)
    )
    conn.commit()
    conn.close()

def atualizar_metas(meta_id, funcionario_id, data, meta):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE metas
        SET funcionario_id = ?, data = ?, meta = ?
        WHERE id = ?
        """,
        (funcionario_id, data, meta, meta_id)
    )

    conn.commit()
    conn.close()

def apontar_realizado(meta_id, realizado):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE metas
    SET realizado = ?
    WHERE id = ?
    """,
        (realizado, meta_id)
    )

    conn.commit()
    conn.close()