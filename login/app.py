from flask import Flask, render_template, request, redirect, url_for
from database import init_db, cadastrar_usuario, verificar_login

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Inicializa o banco de dados
init_db()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        if cadastrar_usuario(usuario, senha):
            return redirect(url_for('login', sucesso=True))
        else:
            return render_template('cadastro.html', erro="Erro ao cadastrar. Usuário pode já existir.")
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        if verificar_login(usuario, senha):
            return render_template('resultado.html', mensagem="Login realizado com sucesso!")
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos.")
    
    sucesso = request.args.get('sucesso')
    return render_template('login.html', sucesso=sucesso)

if __name__ == '__main__':
    app.run(debug=True)