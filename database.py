import sqlite3
from pathlib import Path

DB_NAME = "renewtri.db"


def get_connection():
    """
    Cria a conexão com o banco SQLite.
    Se o arquivo renewtri.db não existir, ele será criado automaticamente.
    """
    return sqlite3.connect(DB_NAME)


def init_db():
    """
    Cria todas as tabelas principais do sistema.
    Essa função será chamada quando o app iniciar.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escolas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            cnpj TEXT NOT NULL UNIQUE,
            inep TEXT NOT NULL,
            senha TEXT NOT NULL,
            codigo_escola TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS merendeiras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            escola_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (escola_id) REFERENCES escolas(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producao_alimentar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            escola_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            turno TEXT NOT NULL,
            refeicoes_produzidas INTEGER NOT NULL,
            alimentos_utilizados TEXT,
            desperdicio_kg REAL NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (escola_id) REFERENCES escolas(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alimentos_recebidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            escola_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            fornecedor TEXT NOT NULL,
            alimento TEXT NOT NULL,
            quantidade_kg REAL NOT NULL,
            validade TEXT,
            observacoes TEXT,
            FOREIGN KEY (escola_id) REFERENCES escolas(id)
        )
    """)

    conn.commit()
    conn.close()


def executar_query(query, params=()):
    """
    Executa comandos INSERT, UPDATE e DELETE.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def buscar_dados(query, params=()):
    """
    Executa comandos SELECT e retorna os resultados.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    dados = cursor.fetchall()
    conn.close()
    return dados


def criar_dados_demo():
    escola_existente = buscar_dados(
        "SELECT id FROM escolas WHERE email = ?",
        ("escola@renewtri.demo",)
    )

    if escola_existente:
        return

    codigo_escola = "ESC-DEMO1"

    executar_query(
        """
        INSERT INTO escolas
        (nome, email, cnpj, inep, senha, codigo_escola)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "CETI Prefeito João Mendes Olímpio de Melo",
            "escola@renewtri.demo",
            "12345678000190",
            "12345678",
            "renewtri123",
            codigo_escola
        )
    )

    escola = buscar_dados(
        "SELECT id FROM escolas WHERE email = ?",
        ("escola@renewtri.demo",)
    )

    escola_id = escola[0][0]

    executar_query(
        """
        INSERT INTO merendeiras
        (escola_id, nome, email, senha, ativo)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            escola_id,
            "Robertina",
            "robertina@renewtri.demo",
            "merenda123",
            1
        )
    )