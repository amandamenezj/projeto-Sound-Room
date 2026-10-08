# SoundRoom — Projeto Flask (Programação para Internet — FATEC Jahu)
# Para rodar: python app.py  ->  http://127.0.0.1:5000

# Flask: cria o app | render_template: monta o HTML da pasta /templates
# request: lê o formulário e o método (GET/POST) | redirect/url_for: vai para outra rota
# session: guarda quem está logado (fica num cookie assinado com a secret_key)
from flask import Flask, render_template, request, redirect, url_for, session
# Guarda a senha embaralhada (hash) em vez do texto puro, e confere na hora do login
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Chave que "assina" o cookie da sessão. Sem ela o Flask não deixa usar session.
app.secret_key = 'soundroom-chave-de-estudo'

# "Banco de dados" simulado: listas de dicionários (cada dicionário = uma linha da tabela).
# Começam VAZIAS: os totais da página Início só contam o que for cadastrado no site.
# Na Aula 05 isso será trocado pelo MySQL. Ao reiniciar o servidor, os dados são perdidos.
usuarios = []   # cada usuário: nome, email, cpf, telefone, senha (hash)
artistas = []   # cada artista: nome, genero, pais, ano_inicio
musicas = []    # cada música: titulo, artista, album, genero, duracao, ano


# Função auxiliar: lê vários campos do formulário de uma vez e devolve um dicionário.
# .get(campo, '') evita o valor None se o campo não vier; .strip() tira espaços das pontas.
def ler_form(*campos):
    return {campo: request.form.get(campo, '').strip() for campo in campos}


# Função auxiliar: procura um usuário pelo e-mail. Devolve o dicionário ou None.
def buscar_usuario(email):
    for u in usuarios:
        if u['email'] == email:
            return u
    return None


# Roda ANTES de toda rota: se não estiver logado, manda para o login.
# O login e os arquivos estáticos ficam liberados para não dar redirecionamento infinito.
@app.before_request
def exigir_login():
    if request.endpoint not in ('login', 'static') and 'email' not in session:
        return redirect(url_for('login'))


# LOGIN (página SEM menu)
# GET = só abrir a página | POST = enviar o formulário. Por isso usamos os dois métodos.
# A mesma rota mostra dois formulários: "entrar" (e-mail + senha) e "cadastrar"
# (nome, CPF, telefone, e-mail + senha). O botão enviado vem em name="acao".
@app.route('/', methods=['GET', 'POST'])
def login():
    mensagem = ''
    modo = request.args.get('modo', 'entrar')    # ?modo=cadastrar abre o formulário de cadastro
    if request.method == 'POST':
        modo = request.form.get('acao')          # 'entrar' ou 'cadastrar'
        senha = request.form.get('senha', '')    # senha não leva strip: espaço pode fazer parte dela

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
                    usuario.update(dados)        # e-mail já existia sem senha: completa os dados
                else:
                    usuarios.append(dados)
                session['email'] = dados['email']    # já deixa a pessoa logada
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
        # Abrir a página de login (ou clicar em "Sair") encerra a sessão
        session.clear()
    return render_template('login.html', mensagem=mensagem, modo=modo)


# INÍCIO (página COM menu)
@app.route('/inicio')
def inicio():
    dados = {
        'total_usuarios': len(usuarios),   # len() conta os itens de cada lista
        'total_artistas': len(artistas),
        'total_musicas': len(musicas),
    }
    # O ** desempacota o dicionário: cada chave vira uma variável no template
    return render_template('inicio.html', **dados)


# USUÁRIOS: a mesma rota lista (GET) e cadastra (POST)
@app.route('/usuarios', methods=['GET', 'POST'])
def pagina_usuarios():
    if request.method == 'POST':
        # Lê os <input name="..."> do formulário
        dados = ler_form('nome', 'email', 'cpf', 'telefone')
        dados['email'] = dados['email'].lower()
        # all(...) é True só se NENHUM campo estiver vazio
        if all(dados.values()):
            existente = buscar_usuario(dados['email'])
            if existente:
                existente.update(dados)    # e-mail já existe: completa os dados (a senha continua)
            else:
                dados['senha'] = ''        # cadastrado aqui, ainda sem senha de login
                usuarios.append(dados)
        # Redireciona após salvar: se apertar F5, o cadastro não é repetido
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


# MÚSICAS: mesma lógica (envia também os artistas para montar o <select>)
@app.route('/musicas', methods=['GET', 'POST'])
def pagina_musicas():
    if request.method == 'POST':
        dados = ler_form('titulo', 'artista', 'album', 'genero', 'duracao', 'ano')
        if all(dados.values()):
            musicas.append(dados)
        return redirect(url_for('pagina_musicas'))
    return render_template('musicas.html', musicas=musicas, artistas=artistas)


if __name__ == '__main__':
    app.run(debug=True)  # debug=True: recarrega sozinho ao salvar e mostra erros
