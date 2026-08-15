from pathlib import Path
import sqlite3

PASTA_DADOS = Path.home() / ".local" / "share" / "SistemaMetas"
PASTA_DADOS.mkdir(parents=True, exist_ok=True)

CAMINHO_BANCO = PASTA_DADOS / "metas.db"


def conectar():
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
def conectar():
    print(f"Banco utilizado: {CAMINHO_BANCO}")

    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

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
    (nome, cargo))

    conn.commit()
    conn.close()

def listar_funcionarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM funcionarios")

    funcionarios = cursor.fetchall()

    conn.close()

    return funcionarios

def excluir_funcionario(meta_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
    "DELETE FROM funcionarios WHERE id = ?",
    (meta_id,))
    conn.commit()
    conn.close()

def atualizar_funcionario(nome, cargo, funcionario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
    "UPDATE funcionarios SET nome = ?, cargo = ? WHERE id = ?",
    (nome, cargo, funcionario_id))
    conn.commit()
    conn.close()

def cadastrar_metas(funcionario_id, data, meta):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO metas (funcionario_id, data, meta) VALUES (?, ?, ?)",
    (funcionario_id, data, meta))
    meta_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return meta_id

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
    ON metas.funcionario_id = funcionarios.id""")

    resultado = cursor.fetchall()

    for linha in resultado:

        meta = linha[3]
        realizado = linha[4]

        if meta > 0:
            porcentagem = (realizado / meta) * 100
        else:
            porcentagem = 0

        print(f"ID: {linha[0]}")
        print(f"Funcionário: {linha[1]}")
        print(f"Data: {linha[2]}")
        print(f"Meta: {meta}")
        print(f"Realizado: {realizado}")
        print(f"Porcentagem Obtida: {porcentagem:.2f}%")
        print("-" * 40)

    conn.close()

    return resultado

def excluir_metas(meta_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
    "DELETE FROM metas WHERE id = ?",
    (meta_id,))

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
    (funcionario_id, data, meta, meta_id))

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
    (realizado, meta_id))

    conn.commit()
    conn.close()

def somar_meta_diaria(data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(meta)
    FROM metas
    WHERE data = ?
    """,
    (data,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado [0] is None:
        return 0

    return resultado[0]

def somar_meta_mes(mes,ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(meta)
    FROM metas
    WHERE strftime('%m', data) = ?
    AND strftime('%Y', data) = ?
    """,
    (mes, ano))

    resultado = cursor.fetchone()

    conn.close()

    if resultado[0] is None:
        return 0

    return resultado[0]

def somar_meta_ano(ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(meta)
    FROM metas
    WHERE strftime('%Y', data) = ?""",
    (ano,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado[0] is None:
        return 0

    return resultado[0]

def somar_realizado_diario(data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(realizado)
    FROM metas
    WHERE data = ?
    """,
    (data,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado[0] is None:
        return 0

    return resultado[0]

def somar_realizado_mes(mes, ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(realizado)
    FROM metas
    WHERE strftime('%m', data) = ?
    AND strftime('%Y', data) = ?
    """,
    (mes, ano))

    resultado = cursor.fetchone()

    conn.close()

    if resultado[0] is None:
        return 0

    return resultado[0]

def somar_realizado_ano(ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(realizado)
    FROM metas
    WHERE strftime('%Y', data) = ?
    """,
    (ano,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado[0] is None:
        return 0

    return resultado[0]

def calcular_porcentagem(realizado, meta):
    if meta <= 0:
        return 0

    return (realizado / meta) * 100

def relatorio_diario(data):
    meta_total = somar_meta_diaria(data)
    realizado_total = somar_realizado_diario(data)
    porcentagem = calcular_porcentagem(realizado_total, meta_total)

    return {
        "meta": meta_total,
        "realizado": realizado_total,
        "porcentagem": porcentagem,
        "bateu_meta": realizado_total >= meta_total and meta_total > 0
    }

def relatorio_mensal(mes, ano):
    meta_total = somar_meta_mes(mes, ano)
    realizado_total = somar_realizado_mes(mes, ano)
    porcentagem = calcular_porcentagem(realizado_total, meta_total)

    return {
        "meta": meta_total,
        "realizado": realizado_total,
        "porcentagem": porcentagem,
        "bateu_meta": realizado_total >= meta_total and meta_total > 0
    }

def relatorio_anual(ano):
    meta_total = somar_meta_ano(ano)
    realizado_total = somar_realizado_ano(ano)
    porcentagem = calcular_porcentagem(realizado_total, meta_total)

    return {
        "meta": meta_total,
        "realizado": realizado_total,
        "porcentagem": porcentagem,
        "bateu_meta": realizado_total >= meta_total and meta_total > 0
    }
criar_tabelas()
