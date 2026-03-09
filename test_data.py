import string
import random
from app import app, db
from models import Autor, Editorial, Libro

with app.app_context():
    # Insert some extra data to test pagination and sorting
    for i in range(15):
        autor = Autor(nombre=f'Autor de prueba {i}', biografia=f'Biografia generada {i}')
        db.session.add(autor)

        ed = Editorial(nombre=f'Editorial Test {i}', pais=random.choice(['España', 'Mexico', 'Argentina']))
        db.session.add(ed)
    
    db.session.commit()

    autores = Autor.query.all()
    editoriales = Editorial.query.all()

    for i in range(25):
        libro = Libro(
            titulo=f'Libro Gen {i}', 
            isbn=f'ISBN-{random.randint(1000, 9999)}', 
            anio=random.randint(1900, 2024),
            autor_id=random.choice(autores).id,
            editorial_id=random.choice(editoriales).id
        )
        db.session.add(libro)
    
    db.session.commit()
    print("Test data inserted")
