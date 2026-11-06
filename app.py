import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request
from flask_wtf.csrf import CSRFProtect

from db import execute_one

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Liga a proteção CSRF: todo formulário POST do sistema vai precisar do token
CSRFProtect(app)

# ==============================================================================
# PÁGINAS PRINCIPAIS
# ==============================================================================

@app.route('/')
def inicio():
    return render_template('login.html')

# GET: abrir pelo menu | POST: vem do formulário de login
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    dados = {
        # TODO (BANCO): SELECT COUNT(*) de cada tabela
        'total_usuarios': 0,
        'total_artistas': 0,
        'total_musicas': 0,
    }
    # O ** desempacota o dicionário: cada chave vira uma variável no template
    return render_template('dashboard.html', **dados)


#  perfis = execute_one('SELECT COUNT(*) AS total FROM perfis')
#     usuarios = execute_one('SELECT COUNT(*) AS total FROM usuarios')
#     produtos = execute_one('SELECT COUNT(*) AS total FROM produtos')

#     return render_template('dashboard.html', titulo='Sistema de Gestão',
#                            total_perfis=perfis['total'],
#                            total_usuarios=usuarios['total'],
#                            total_produtos=produtos['total'])

# ==============================================================================
# USUARIOS
# ==============================================================================

@app.route('/usuarios/listar')
def listar_usuarios():
    return render_template('usuarios/usuarios_listar.html')

@app.route('/usuarios/inserir')
def inserir_usuario():
    return render_template('usuarios/usuarios_form.html')

# ==============================================================================
# ARTISTAS
# ==============================================================================

@app.route('/artistas/listar')
def listar_artistas():
    return render_template('artistas/artistas-listar.html')

@app.route('/artistas/inserir')
def inserir_artista():
    return render_template('artistas/artistas-form.html')

# ==============================================================================
# MUSICAS
# ==============================================================================

@app.route('/musicas/listar')
def listar_musicas():
    return render_template('musicas/musicas-listar.html')

@app.route('/musicas/inserir')
def inserir_musica():
    return render_template('musicas/musicas-form.html')


# ==============================================================================
# PERFIS
# ==============================================================================

@app.route('/perfis/listar', method=['GET', 'POST'])
def listar_perfil():

    if request.method == 'POST':
        redirect(url_for(listar_perfil))

    return render_template('perfis/perfil-listar.html')


@app.route('/perfis/inserir')
def inserir_perfil():
    return render_template('perfis/perfil-form.html')








# ==============================================================================
# TELAS DE ERROS
# ==============================================================================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)  # debug=True: recarrega sozinho ao salvar e mostra erros
