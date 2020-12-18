# Importar utilidades del sistema operativo
import os
# Importar utilidades de encriptacion
import hashlib

# De esta manera se importan la librerias que vamos a utilizar
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Se obtiene la ruta de la carpeta donde se encuentra el proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))
# Se estable la ruta de la base de datos
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tarea.db"))

# Se crea la instancia de Flask
app = Flask(__name__)
# Se le asigna la conexion de la base de datos al contexto Flask
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
# SE inactivan el analisis de cambios
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Se crea una instancia para manejar la base de datos
db = SQLAlchemy(app)

# ***********************************
# * AREA PARA DECLARACION DE CLASES *
# ***********************************
# Clase para administrar las tareas
class Tarea(db.Model):
    # Propiedades de la tabla
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    realizada = db.Column(db.Boolean, nullable=False)
    # Metodo constructor de la clase
    def __init__(self, nombre, realizada):
        self.nombre = nombre
        self.realizada = realizada

# Clase para administrar usuarios del sistema
class Usuario(db.Model):
    # Propiedades de la tabla
    email = db.Column(db.String(150), nullable=False, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150))
    # Metodo constructor de la clase
    def __init__(self, email, nombre, password):
        self.email = email
        self.nombre = nombre
        self.password = password

# Clase para administrar mensajes del sistema
class Mensaje:
    # Metodo constructor de la clase
    def __init__(self, css, titulo, texto, esError):
        self.css = css
        self.titulo = titulo
        self.texto = texto
        self.esError = esError

# **************************************
# * AREA PARA DECLARACION DE VARIABLES *
# **************************************
# Flag de sesion activa (Variable Global)
sesion = False

# Usuario conectado (Variable Global)
usuario = None

# **************************************
# * AREA PARA DECLARACION DE FUNCIONES *
# **************************************
# +---------------------------------------------+
# | Funcion que se encarga de la vista de login |
# +---------------------------------------------+
@app.route("/", methods=["GET", "POST"])
def login():
    # Declaracion para uso de variables globales
    global sesion
    global usuario
    # Si la sesion esta activa se redirige a la vista de tareas
    if sesion:
        # Se consultan todas las tareas en la base de datos
        tareas = Tarea.query.all()
        return render_template("tareas.html", usuario=usuario, tareas=tareas)
    mensaje = Mensaje("alert-info", "", "", False)
    # Se verifica que verbo HTTP se utilizo para la peticion. Si es POST es el formulario, si es GET es desde la URL
    if request.method == "GET":
        return render_template("login.html", mensaje=mensaje)
    else:
        # Se obtienen los datos del formulario
        email = request.form.get("email")
        password = request.form.get("password")

        # Se encripta el password para compararlo con el de la base de datos
        criptoPassword = hashlib.sha256(str(password).encode('utf-8')).hexdigest()

        # Se busca si el usuario se encuentra registrado y su contraseña esta correcta
        usuario = Usuario.query.filter_by(email=email, password=criptoPassword).first()

        # Validacion del usuario
        if usuario != None:
            # Se establece la variable sesion en verdadero
            sesion = True
            # Se consultan todas las tareas en la base de datos
            tareas = Tarea.query.all()
            return render_template("tareas.html", usuario=usuario, tareas=tareas)
        else:
            mensaje = Mensaje("alert-danger", "Validación", "Correo Electronico y/o Contraseña estan errados.", True)
            return render_template("login.html", mensaje=mensaje)

# +----------------------------------------------+
# | Funcion que se encarga de la vista de tareas |
# +----------------------------------------------+
@app.route("/tareas")
def tareas():
    # Declaracion para uso de variables globales
    global sesion
    global usuario
    # Si la sesion esta activa se redirige a la vista de tareas
    if sesion:
        # Se consultan todas las tareas en la base de datos
        tareas = Tarea.query.all()
        return render_template("tareas.html", usuario=usuario, tareas=tareas)
    else:
        mensaje = Mensaje("alert-info", "Sin Sesion", "Sesion Expirada", True)
        return render_template("login.html", mensaje=mensaje)

# +--------------------------------------------+
# | Funcion que se encarga de cerrar la sesion |
# +--------------------------------------------+
@app.route("/salir")
def salir():
    # Declaracion para uso de variables globales
    global sesion
    global usuario
    sesion = False
    usuario = None
    mensaje = Mensaje("alert-info", "Sin Sesion", "Sesion Terminada", True)
    return render_template("login.html", mensaje=mensaje)

# +----------------------------------------+
# | Funcion que se encarga de crear tareas |
# +----------------------------------------+
@app.route("/crear", methods=["GET", "POST"])
def crear():
    # Declaracion para uso de variables globales
    global usuario
    global sesion

    mensaje = Mensaje("alert-info", "", "", False)

    # Se verifica la sesion, sino esta activa se redirige al login
    if not sesion:
        mensaje = Mensaje("alert-info", "Sin Sesion", "Sesion Expirada", True)
        return render_template("login.html", mensaje=mensaje)

    # Se verifica que verbo HTTP se utilizo para la peticion. Si es POST es el formulario, si es GET es desde la URL
    if request.method == "GET":
        return render_template("crear.html", usuario=usuario, mensaje=mensaje)
    else:
        # Se obtienen los datos del formulario
        nombre = request.form.get("nombre")

        # Consultar si la tarea ya existe
        tarea = Tarea.query.filter_by(nombre=nombre).first()

        if tarea == None:
            # Se inserta la nueva tarea
            try:
                tarea = Tarea(nombre, False)
                db.session.add(tarea)
                db.session.commit()
            except Exception as e:
                print(e)

        # Se consultan todas las tareas en la base de datos
        tareas = Tarea.query.all()
        return render_template("tareas.html", usuario=usuario, tareas=tareas)

# +-------------------------------------------+
# | Funcion que se encarga de eliminar tareas |
# +-------------------------------------------+
@app.route("/tarea/d/<int:id>")
def eliminar(id):
    # Declaracion para uso de variables globales
    global usuario
    global sesion

    mensaje = Mensaje("alert-info", "", "", False)

    # Se verifica la sesion, sino esta activa se redirige al login
    if not sesion:
        mensaje = Mensaje("alert-info", "Sin Sesion", "Sesion Expirada", True)
        return render_template("login.html", mensaje=mensaje)

    # Se busca si el usuario se encuentra registrado y su contraseña esta correcta
    tarea = Tarea.query.filter_by(id=id).first()
    if tarea != None:
        # Se elimina la tarea
        try:
            db.session.delete(tarea)
            db.session.commit()
        except Exception as e:
            print(e)

    # Se consultan todas las tareas en la base de datos
    tareas = Tarea.query.all()
    return render_template("tareas.html", usuario=usuario, tareas=tareas)

# +---------------------------------------------+
# | Funcion que se encarga de actualizar tareas |
# +---------------------------------------------+
@app.route("/tarea/u/<int:id>")
def actualizar(id):
    # Declaracion para uso de variables globales
    global usuario
    global sesion

    mensaje = Mensaje("alert-info", "", "", False)

    # Se verifica la sesion, sino esta activa se redirige al login
    if not sesion:
        mensaje = Mensaje("alert-info", "Sin Sesion", "Sesion Expirada", True)
        return render_template("login.html", mensaje=mensaje)

    # Se busca si el usuario se encuentra registrado y su contraseña esta correcta
    tarea = Tarea.query.filter_by(id=id).first()
    if tarea != None:
        # Se actualiza la tarea
        try:
            tarea.realizada = not tarea.realizada
            db.session.commit()
        except Exception as e:
            print(e)

    # Se consultan todas las tareas en la base de datos
    tareas = Tarea.query.all()
    return render_template("tareas.html", usuario=usuario, tareas=tareas)

@app.route("/prueba")
def prueba():
    # Declaracion para uso de variables globales
    global usuario
    return render_template("prueba.html", usuario=usuario)

# Activar el modo debug de la aplicacion
if __name__ == "__main__":
    app.run(debug=True)