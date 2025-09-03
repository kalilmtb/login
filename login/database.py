import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def cadastrar_usuario(usuario, senha):
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        
        # Criptografa a senha antes de salvar
        senha_hash = generate_password_hash(senha)
        
        cursor.execute(
            'INSERT INTO usuarios (usuario, senha) VALUES (?, ?)',
            (usuario, senha_hash)
        )
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Usuário já existe
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")
        return False

def verificar_login(usuario, senha):
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT senha FROM usuarios WHERE usuario = ?',
            (usuario,)
        )
        
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado and check_password_hash(resultado[0], senha):
            return True
        return False
        
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
        return False