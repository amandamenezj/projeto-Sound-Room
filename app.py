# SoundRoom — Projeto Flask (Programação para Internet — FATEC Jahu)
# Para rodar: python app.py  ->  http://127.0.0.1:5000

# Flask: cria o app | render_template: monta o HTML da pasta /templates
# request: lê o formulário e o método (GET/POST) | redirect/url_for: vai para outra rota
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# "Banco de dados" simulado: listas de dicionários (cada dicionário = uma linha da tabela).
# Na Aula 05 isso será trocado pelo MySQL. Ao reiniciar o servidor, os dados voltam ao início.
usuarios = []
artistas = [
    {'nome': 'Sabrina Carpenter', 'genero': 'Pop', 'pais': 'Estados Unidos', 'ano_inicio': 2011},
    {'nome': 'Arctic Monkeys', 'genero': 'Indie Rock', 'pais': 'Reino Unido', 'ano_inicio': 2002},
]
musicas = [
    {'titulo': 'Espresso', 'artista': 'Sabrina Carpenter', 'album': "Short n' Sweet",
     'genero': 'Pop', 'duracao': '2:55', 'ano': 2024},
    {'titulo': '505', 'artista': 'Arctic Monkeys', 'album': 'Favourite Worst Nightmare',
     'genero': 'Indie', 'duracao': '4:13', 'ano': 2007},
]


# Função auxiliar: lê vários campos do formulário de uma vez e devolve um dicionário.
# .get(campo, '') evita o valor None se o campo não vier; .strip() tira espaços das pontas.
def ler_form(*campos):
    return {campo: request.form.get(campo, '').strip() for campo in campos}


# LOGIN (página SEM menu)
# GET = só abrir a página | POST = enviar o formulário. Por isso usamos os dois métodos.
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ainda sem banco: qualquer login vai para o início.
        return redirect(url_for('inicio'))
    return render_template('login.html')


# INÍCIO (página COM menu).
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
        # all(...) é True só se NENHUM campo estiver vazio
        if all(dados.values()):
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

# Tudo funcionando até o ultimo teste

if __name__ == '__main__':
    app.run(debug=True)  # debug=True: recarrega sozinho ao salvar e mostra erros
