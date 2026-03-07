from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Autor(db.Model):
    __tablename__ = 'autores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    biografia = db.Column(db.Text)
    libros = db.relationship('Libro', backref='autor', lazy=True)

class Editorial(db.Model):
    __tablename__ = 'editoriales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(50))
    libros = db.relationship('Libro', backref='editorial', lazy=True)

class Libro(db.Model):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    anio = db.Column(db.Integer)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)
    editorial_id = db.Column(db.Integer, db.ForeignKey('editoriales.id'), nullable=False)
