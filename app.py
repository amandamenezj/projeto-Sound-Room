# SoundRoom — Projeto Flask (Programação para Internet — FATEC Jahu)
# Para rodar: python app.py  ->  http://127.0.0.1:5000
#
# VERSÃO SEM BANCO DE DADOS: tudo que lia/gravava no banco está marcado com "TODO (BANCO)".
# É nesses pontos que a conexão e os comandos SQL vão entrar.

# Flask: cria o app | render_template: monta o HTML da pasta /templates
# request: lê o formulário e o método (GET/POST) | redirect/url_for: vai para outra rota
# session: guarda quem está logado (fica num cookie assinado com a secret_key)
from flask import Flask, render_template, request, redirect, url_for, session
# Guarda a senha embaralhada (hash) em vez do texto puro, e confere na hora do login
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Chave que "assina" o cookie da sessão. Sem ela o Flask não deixa usar session.
app.secret_key = 'soundroom-chave-de-estudo'

# TODO (BANCO): criar aqui a conexão com o banco (ex.: mysql.connector.connect(...)).
# Tabelas previstas:
#   usuarios: nome, email, cpf, telefone, senha (hash)
#   artistas: nome, genero, pais, ano_inicio
#   musicas : titulo, artista, album, genero, duracao, ano


# Função auxiliar: lê vários campos do formulário de uma vez e devolve um dicionário.
# .get(campo, '') evita o valor None se o campo não vier; .strip() tira espaços das pontas.
def ler_form(*campos):
    return {campo: request.form.get(campo, '').strip() for campo in campos}


# Função auxiliar: procura um usuário pelo e-mail. Devolve o dicionário ou None.
def buscar_usuario(email):
    # TODO (BANCO): SELECT * FROM usuarios WHERE email = %s
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
                # TODO (BANCO): se o usuário já existe (sem senha), UPDATE; senão, INSERT INTO usuarios
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
        # TODO (BANCO): SELECT COUNT(*) de cada tabela
        'total_usuarios': 0,
        'total_artistas': 0,
        'total_musicas': 0,
    }
    # O ** desempacota o dicionário: cada chave vira uma variável no template
    return render_template('inicio.html', **dados)


# USUÁRIOS: a mesma rota lista (GET), cadastra, edita e exclui (POST)
@app.route('/usuarios/listar', methods=['GET', 'POST'])
def pagina_usuarios():
    if request.method == 'POST':
        if 'excluir' in request.form:
            # TODO (BANCO): DELETE FROM usuarios WHERE ...
            # Se a pessoa excluiu a própria conta, encerrar a sessão: session.clear()
            pass
        else:
            # Lê os <input name="..."> do formulário
            dados = ler_form('nome', 'email', 'cpf', 'telefone')
            dados['email'] = dados['email'].lower()
            # all(...) é True só se NENHUM campo estiver vazio
            if all(dados.values()):
                # TODO (BANCO): se veio o campo escondido "indice" -> UPDATE (o e-mail não muda);
                #               senão -> INSERT INTO usuarios (senha vazia: ainda sem login)
                pass
        # Redireciona após salvar: se apertar F5, a ação não é repetida
        return redirect(url_for('pagina_usuarios'))
    # TODO (BANCO): SELECT * FROM usuarios
    # TODO (BANCO): se vier ?editar=..., buscar o registro para preencher o formulário (edicao)
    return render_template('usuarios/usuarios_listar.html', usuarios=[], indice=None, edicao={})


# ARTISTAS: mesma lógica
@app.route('/artistas', methods=['GET', 'POST'])
def pagina_artistas():
    if request.method == 'POST':
        if 'excluir' in request.form:
            # TODO (BANCO): DELETE FROM artistas WHERE ...
            # (antes: apagava também as músicas do artista -> ON DELETE CASCADE ou DELETE manual)
            pass
        else:
            dados = ler_form('nome', 'genero', 'pais', 'ano_inicio')
            if all(dados.values()):
                # TODO (BANCO): UPDATE (se veio "indice") ou INSERT INTO artistas
                # (antes: se o nome mudava, as músicas do artista passavam a usar o nome novo)
                pass
        return redirect(url_for('pagina_artistas'))
    # TODO (BANCO): SELECT * FROM artistas  +  registro em edição (?editar=...)
    return render_template('artistas.html', artistas=[], indice=None, edicao={})


# MÚSICAS: mesma lógica (envia também os artistas para montar o <select>)
@app.route('/musicas', methods=['GET', 'POST'])
def pagina_musicas():
    if request.method == 'POST':
        if 'excluir' in request.form:
            # TODO (BANCO): DELETE FROM musicas WHERE ...
            pass
        else:
            dados = ler_form('titulo', 'artista', 'album', 'genero', 'duracao', 'ano')
            if all(dados.values()):
                # TODO (BANCO): UPDATE (se veio "indice") ou INSERT INTO musicas
                pass
        return redirect(url_for('pagina_musicas'))
    # TODO (BANCO): SELECT * FROM musicas  +  SELECT * FROM artistas (para o <select>)  +  registro em edição
    return render_template('musicas.html', musicas=[], artistas=[], indice=None, edicao={})

    


if __name__ == '__main__':
    app.run(debug=True)  # debug=True: recarrega sozinho ao salvar e mostra erros
