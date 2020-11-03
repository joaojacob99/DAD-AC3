from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cliente.db"
#app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://postgres:root@localhost:5432/DBImpacta"

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    comment = db.Column(db.String(120))

    def __init__(self, name, comment):
        self.name = name 
        self.comment = comment 

@app.route("/")
def index():
    clientes = Cliente.query.all()
    return render_template("index.html", clientes=clientes)

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        cliente = Cliente(request.form['nome'], request.form['comentario'])
        db.session.add(cliente)
        db.session.commit() 
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    cliente = Cliente.query.get(id)
    if request.method == 'POST':
        cliente.name = request.form['nome']
        cliente.comment = request.form['comentario']
        db.session.commit() 
        return redirect(url_for('index'))
    return render_template('edit.html', cliente=cliente)

@app.route("/delete/<int:id>")
def delete(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit() 
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True) 
