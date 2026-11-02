from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/usuarios/listar')
def listar_usuarios():
    return render_template('usuarios/usuarios_listar.html')

@app.route('/usuarios/inserir')
def inserir_usuario():
    return render_template('usuarios/usuarios_form.html')

@app.route('/artistas/listar')
def listar_artistas():
    return render_template('artistas/artistas-listar.html')

@app.route('/artistas/inserir')
def inserir_artista():
    return render_template('artistas/artistas-form.html')

@app.route('/musicas/listar')
def listar_musicas():
    return render_template('musicas/musicas-listar.html')

@app.route('/musicas/inserir')
def inserir_musica():
    return render_template('musicas/musicas-form.html')




if __name__ == '__main__':
    app.run(debug=True)  # debug=True: recarrega sozinho ao salvar e mostra erros
