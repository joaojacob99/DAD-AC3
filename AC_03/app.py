from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cliente.db"
#app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://postgres:root@localhost:5432/DBImpacta"
db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = "tbaluno"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ra = db.Column(db.Integer, unique=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    logradouro = db.Column(db.String(50))
    numero = db.Column(db.String(10))
    cep = db.Column(db.String(10))
    bairro = db.Column(db.String(20))

    def __init__(self, ra, nome, email, logradouro, numero, cep, bairro):
        self.ra = ra
        self.nome = nome
        self.email = email
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.bairro = bairro

@app.route("/")
def index():
    alunos = Aluno.query.all()
    return render_template("index.html", alunos=alunos)


@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        aluno = Aluno(request.form['ra'],
                      request.form['nome'],
                      request.form['email'],
                      request.form['logradouro'],
                      request.form['numero'],
                      request.form['cep'],
                      request.form['bairro'])
        db.session.add(aluno)
        db.session.commit() 
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    aluno = Aluno.query.get(id)
    if request.method == 'POST':
        aluno.ra = request.form['ra']
        aluno.nome = request.form['nome']
        aluno.email = request.form['email']
        aluno.logradouro = request.form['logradouro']
        aluno.numero = request.form['numero']
        aluno.cep = request.form['cep']
        aluno.bairro = request.form['bairro']

        db.session.commit() 
        return redirect(url_for('index'))
    return render_template('edit.html', aluno=aluno)

@app.route("/delete/<int:id>")
def delete(id):
    aluno = Aluno.query.get(id)
    db.session.delete(aluno)
    db.session.commit() 
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True) 
