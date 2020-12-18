# TareasFlaskDb
Ejemplo desarrollado en FlasK para la creación de tareas con bases de datos. Para ejecutar la pagina se debe realizar el siguiernte comando:

```console
pip install Flask Flask-SQLAlchemy SQLAlchemy
python app.py
```

```sql
CREATE TABLE tarea (
    id        INTEGER       PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    nombre    VARCHAR (150) UNIQUE NOT NULL,
    realizada BOOLEAN       NOT NULL
);

CREATE TABLE usuario (
    email    VARCHAR (150) PRIMARY KEY UNIQUE NOT NULL,
    nombre   VARCHAR (150) UNIQUE NOT NULL,
    password VARCHAR (150) 
);

INSERT INTO usuario
VALUES ('admin@tasks.com'
       ,'Administrador del Sistema'
       ,'8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92');
```

* https://www.python.org/downloads/
* https://www.w3schools.com/python/default.asp
* https://flask.palletsprojects.com/en/1.1.x/installation/#installation
* https://dbdiagram.io/d/
* https://entrenamiento-frameworks-web-python.readthedocs.io/es/latest/leccion6/crud_app.html
* https://www.youtube.com/channel/UCNdy_LQjD_ew3r5zEXOA0aQ
* https://www.youtube.com/watch?v=7s1RjItUBqU&list=PLL0TiOXBeDagsYUYFO9WMwDtuDuoGZVB9&ab_channel=Fazt
