# SoundRoom — Projeto Flask (Programação para Internet — FATEC Jahu)
# Para rodar: python app.py  ->  http://127.0.0.1:5000

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'soundroom-chave-de-estudo'

usuarios = []   # cada usuário: nome, email, cpf, telefone, senha (hash)
artistas = []   # cada artista: nome, genero, pais, ano_inicio
musicas = []    # cada música: titulo, artista, album, genero, duracao, ano


def ler_form(*campos):
    return {campo: request.form.get(campo, '').strip() for campo in campos}


def buscar_usuario(email):
    for u in usuarios:
        if u['email'] == email:
            return u
    return None

@app.before_request
def exigir_login():
    if request.endpoint not in ('login', 'static') and 'email' not in session:
        return redirect(url_for('login'))


# LOGIN (página SEM menu)
@app.route('/', methods=['GET', 'POST'])
def login():
    mensagem = ''
    modo = request.args.get('modo', 'entrar')   
    if request.method == 'POST':
        modo = request.form.get('acao')          # 'entrar' ou 'cadastrar'
        senha = request.form.get('senha', '')    

        if modo == 'cadastrar':
            dados = ler_form('nome', 'cpf', 'telefone', 'email')
            dados['email'] = dados['email'].lower()
            usuario = buscar_usuario(dados['email'])
            if not all(dados.values()) or not senha:
                mensagem = 'Preencha todos os campos.'
            elif usuario and usuario['senha']:
                mensagem = 'Este e-mail já está cadastrado. Clique em Entrar.'
            else:
                dados['senha'] = generate_password_hash(senha)
                if usuario:
                    usuario.update(dados)        
                else:
                    usuarios.append(dados)
                session['email'] = dados['email']    
                return redirect(url_for('inicio'))
        else:  # modo == 'entrar'
            email = request.form.get('email', '').strip().lower()
            usuario = buscar_usuario(email)
            if usuario is None:
                mensagem = 'E-mail não cadastrado. Clique em "Criar conta" para se cadastrar.'
            elif not usuario['senha']:
                mensagem = 'Este e-mail ainda não tem senha. Crie sua conta para definir uma.'
            elif check_password_hash(usuario['senha'], senha):
                session['email'] = email
                return redirect(url_for('inicio'))
            else:
                mensagem = 'Senha incorreta.'
    else:
        
        session.clear()
    return render_template('login.html', mensagem=mensagem, modo=modo)


# INÍCIO (página COM menu)
@app.route('/inicio')
def inicio():
    dados = {
        'total_usuarios': len(usuarios),   
        'total_artistas': len(artistas),
        'total_musicas': len(musicas),
    }
  
    return render_template('inicio.html', **dados)


# USUÁRIOS
@app.route('/usuarios', methods=['GET', 'POST'])
def pagina_usuarios():
    if request.method == 'POST':
        
        dados = ler_form('nome', 'email', 'cpf', 'telefone')
        dados['email'] = dados['email'].lower()
      
        if all(dados.values()):
            existente = buscar_usuario(dados['email'])
            if existente:
                existente.update(dados)    
            else:
                dados['senha'] = ''       
                usuarios.append(dados)
       
        return redirect(url_for('pagina_usuarios'))
    return render_template('usuarios.html', usuarios=usuarios)


# ARTISTAS: mesma lógica
@app.route('/artistas', methods=['GET', 'POST'])
def pagina_artistas():
    if request.method == 'POST':
        dados = ler_form('nome', 'genero', 'pais', 'ano_inicio')
        if all(dados.values()):
            artistas.append(dados)
        return redirect(url_for('pagina_artistas'))
    return render_template('artistas.html', artistas=artistas)


# MÚSICAS: mesma lógica 
@app.route('/musicas', methods=['GET', 'POST'])
def pagina_musicas():
    if request.method == 'POST':
        dados = ler_form('titulo', 'artista', 'album', 'genero', 'duracao', 'ano')
        if all(dados.values()):
            musicas.append(dados)
        return redirect(url_for('pagina_musicas'))
    return render_template('musicas.html', musicas=musicas, artistas=artistas)


if __name__ == '__main__':
    app.run(debug=True)  
