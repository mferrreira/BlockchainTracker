import sqlite3
from flask import Flask

app = Flask(__name__)

DATABASE = 'blockchain_monitor.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acessar as colunas como dicionários
    return conn

# Criação das tabelas, caso não existam
def init_db():
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_id INTEGER,
                transaction_hash TEXT UNIQUE NOT NULL,
                amount REAL,
                timestamp TIMESTAMP NOT NULL,
                type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (wallet_id) REFERENCES wallets(id)
            );
        """)
        db.commit()

# Rota para inicializar o banco
@app.route('/init_db')
def init_database():
    init_db()
    return "Database initialized!"

if __name__ == '__main__':
    app.run(debug=True)
