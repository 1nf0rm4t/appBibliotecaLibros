from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Autor, Editorial, Libro, Usuario

import os
import dotenv

app = Flask(__name__)

dotenv.load_dotenv()

# Configuración para MariaDB
# Formato: mysql+pymysql://usuario:contrasena@servidor:puerto/nombre_bd
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'mysql+pymysql://root:password@127.0.0.1:3306/biblioteca'
)



#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SECRET_KEY'] = 'biblioteca-secret-key'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, inicie sesión para acceder a esta página."
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
    
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/')
def index():
    return render_template('base.html')
    
# ==================== AUTENTICACIÓN ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            
    return render_template('auth/login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_exists = Usuario.query.filter_by(username=username).first()
        if user_exists:
            flash('El nombre de usuario ya está en uso', 'error')
            return redirect(url_for('registro'))
            
        new_user = Usuario(
            username=username, 
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registro completado. Por favor, inicie sesión.', 'success')
        return redirect(url_for('login'))
        
    return render_template('auth/registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
def index():
    return render_template('base.html')

# ==================== AUTORES ====================
from sqlalchemy import or_

@app.route('/autores')
@login_required
def autores_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    query = Autor.query

    if q:
        search_term = f"%{q}%"
        query = query.filter(or_(Autor.nombre.ilike(search_term), Autor.biografia.ilike(search_term)))

    if sort == 'nombre':
        query = query.order_by(Autor.nombre.desc() if order == 'desc' else Autor.nombre.asc())
    elif sort == 'biografia':
        query = query.order_by(Autor.biografia.desc() if order == 'desc' else Autor.biografia.asc())
    else:
        query = query.order_by(Autor.id.desc() if order == 'desc' else Autor.id.asc())

    autores = query.paginate(page=page, per_page=10, error_out=False)
    return render_template('autores/list.html', autores=autores, q=q, sort=sort, order=order)

@app.route('/autores/nuevo', methods=['GET', 'POST'])
@login_required
def autores_new():
    if request.method == 'POST':
        autor = Autor(
            nombre=request.form['nombre'],
            biografia=request.form['biografia']
        )
        db.session.add(autor)
        db.session.commit()
        flash('Autor creado exitosamente', 'success')
        return redirect(url_for('autores_list'))
    return render_template('autores/form.html', autor=None)

@app.route('/autores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def autores_edit(id):
    autor = Autor.query.get_or_404(id)
    if request.method == 'POST':
        autor.nombre = request.form['nombre']
        autor.biografia = request.form['biografia']
        db.session.commit()
        flash('Autor actualizado exitosamente', 'success')
        return redirect(url_for('autores_list'))
    return render_template('autores/form.html', autor=autor)

@app.route('/autores/eliminar/<int:id>')
@login_required
def autores_delete(id):
    autor = Autor.query.get_or_404(id)
    db.session.delete(autor)
    db.session.commit()
    flash('Autor eliminado exitosamente', 'success')
    return redirect(url_for('autores_list'))

# ==================== EDITORIALES ====================
@app.route('/editoriales')
@login_required
def editoriales_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    query = Editorial.query

    if q:
        search_term = f"%{q}%"
        query = query.filter(or_(Editorial.nombre.ilike(search_term), Editorial.pais.ilike(search_term)))

    if sort == 'nombre':
        query = query.order_by(Editorial.nombre.desc() if order == 'desc' else Editorial.nombre.asc())
    elif sort == 'pais':
        query = query.order_by(Editorial.pais.desc() if order == 'desc' else Editorial.pais.asc())
    else:
        query = query.order_by(Editorial.id.desc() if order == 'desc' else Editorial.id.asc())

    editoriales = query.paginate(page=page, per_page=10, error_out=False)
    return render_template('editoriales/list.html', editoriales=editoriales, q=q, sort=sort, order=order)

@app.route('/editoriales/nueva', methods=['GET', 'POST'])
@login_required
def editoriales_new():
    if request.method == 'POST':
        editorial = Editorial(
            nombre=request.form['nombre'],
            pais=request.form['pais']
        )
        db.session.add(editorial)
        db.session.commit()
        flash('Editorial creada exitosamente', 'success')
        return redirect(url_for('editoriales_list'))
    return render_template('editoriales/form.html', editorial=None)

@app.route('/editoriales/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editoriales_edit(id):
    editorial = Editorial.query.get_or_404(id)
    if request.method == 'POST':
        editorial.nombre = request.form['nombre']
        editorial.pais = request.form['pais']
        db.session.commit()
        flash('Editorial actualizada exitosamente', 'success')
        return redirect(url_for('editoriales_list'))
    return render_template('editoriales/form.html', editorial=editorial)

@app.route('/editoriales/eliminar/<int:id>')
@login_required
def editoriales_delete(id):
    editorial = Editorial.query.get_or_404(id)
    db.session.delete(editorial)
    db.session.commit()
    flash('Editorial eliminada exitosamente', 'success')
    return redirect(url_for('editoriales_list'))

# ==================== LIBROS ====================
@app.route('/libros')
@login_required
def libros_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    query = Libro.query.join(Autor).join(Editorial)

    if q:
        search_term = f"%{q}%"
        query = query.filter(or_(
            Libro.titulo.ilike(search_term), 
            Libro.isbn.ilike(search_term),
            Autor.nombre.ilike(search_term),
            Editorial.nombre.ilike(search_term)
        ))

    if sort == 'titulo':
        query = query.order_by(Libro.titulo.desc() if order == 'desc' else Libro.titulo.asc())
    elif sort == 'isbn':
        query = query.order_by(Libro.isbn.desc() if order == 'desc' else Libro.isbn.asc())
    elif sort == 'anio':
        query = query.order_by(Libro.anio.desc() if order == 'desc' else Libro.anio.asc())
    elif sort == 'autor':
        query = query.order_by(Autor.nombre.desc() if order == 'desc' else Autor.nombre.asc())
    elif sort == 'editorial':
        query = query.order_by(Editorial.nombre.desc() if order == 'desc' else Editorial.nombre.asc())
    else:
        query = query.order_by(Libro.id.desc() if order == 'desc' else Libro.id.asc())

    libros = query.paginate(page=page, per_page=10, error_out=False)
    return render_template('libros/list.html', libros=libros, q=q, sort=sort, order=order)

@app.route('/libros/nuevo', methods=['GET', 'POST'])
@login_required
def libros_new():
    autores = Autor.query.all()
    editoriales = Editorial.query.all()
    if request.method == 'POST':
        libro = Libro(
            titulo=request.form['titulo'],
            isbn=request.form['isbn'],
            anio=request.form['anio'],
            autor_id=request.form['autor_id'],
            editorial_id=request.form['editorial_id']
        )
        db.session.add(libro)
        db.session.commit()
        flash('Libro creado exitosamente', 'success')
        return redirect(url_for('libros_list'))
    return render_template('libros/form.html', libro=None, autores=autores, editoriales=editoriales)

@app.route('/libros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def libros_edit(id):
    libro = Libro.query.get_or_404(id)
    autores = Autor.query.all()
    editoriales = Editorial.query.all()
    if request.method == 'POST':
        libro.titulo = request.form['titulo']
        libro.isbn = request.form['isbn']
        libro.anio = request.form['anio']
        libro.autor_id = request.form['autor_id']
        libro.editorial_id = request.form['editorial_id']
        db.session.commit()
        flash('Libro actualizado exitosamente', 'success')
        return redirect(url_for('libros_list'))
    return render_template('libros/form.html', libro=libro, autores=autores, editoriales=editoriales)

@app.route('/libros/eliminar/<int:id>')
@login_required
def libros_delete(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado exitosamente', 'success')
    return redirect(url_for('libros_list'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
