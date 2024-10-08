import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Função para inicializar o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT,
            ano_publicacao INTEGER,
            isbn TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Chamar a função para inicializar o banco de dados
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    conn.close()
    return render_template('index.html', livros=livros)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        editora = request.form['editora']
        ano_publicacao = request.form['ano_publicacao']
        isbn = request.form['isbn']

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, autor, editora, ano_publicacao, isbn))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('adicionar.html')

@app.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    if request.method == 'POST':
        termo_pesquisa = request.form['termo_pesquisa']
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM livros WHERE titulo LIKE ?', ('%' + termo_pesquisa + '%',))
        livros = cursor.fetchall()
        conn.close()
        return render_template('pesquisar.html', livros=livros)
    
    return render_template('pesquisar.html')

if __name__ == '__main__':
    app.run(debug=True)
