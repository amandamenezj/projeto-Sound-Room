from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/usuarios/listar')
def listar_usuarios():
    return render_template ('usuarios/usuarios-listar.html')

@app.route('/usuarios/inserir')
def inserir_usuario():
    return render_template('usuarios/usuarios-form.html')   

@app.route('/artistas/listar')
def listar_artistas():
    return render_template('aristas/artistas-listar.html')

@app.route('/artistas/inserir')
def listar_artistas():
    return render_template('aristas/artistas-form.html')

@app.route('/musicas/listar')
def listar_artistas():
    return render_template('musicas/musicas-listar.html')

@app.route('/musicas/inserir')
def listar_artistas():
    return render_template('musicas/musicas-form.html')




if __name__ == '__main__':
    app.run(debug=True)  # debug=True: recarrega sozinho ao salvar e mostra erros
