import json
import mimetypes
import time
import datetime

from flask import Flask, url_for, request, render_template, redirect
from markupsafe import escape

app = Flask(__name__)

#
@app.route('/<nombre>')
def hola(nombre):
    return f'Hello, {escape(nombre)}!'

# URL única, al añadir la barra final, si no la escribimos al escribir la ruta
# no redirige igualmente
@app.route('/llamar/')
def llamar():
    return f'Me llamo Jaime!'

# Ruta raiz
@app.route('/index')
def index():
    return 'index.html'

# URL única, si añadimos una barra al final no saldrá un mensaje 404 NOT FOUND
@app.route('/hello')
def hello():
    return 'Hello, Woradfadfafafald'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

# Se pasa como parámetro el nombre de la función y se escribe la ruta como se ha definido
with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello'))
    print(url_for('hola', nombre='Jaime'))
    print(url_for('show_user_profile', username='Oliver'))

#@app.route('/login', methods = ['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        return login_post()
#    else:
#        return login_get()

# Método HTTP GET
@app.get('/login')
def login_get():
    return render_template('login.html')

@app.route('/secreto')
def secreto():
    return render_template('secreto.html')

@app.route('/normal')
def normal():
    return render_template('normal.html')

@app.route('/nombrado/<nombre>')
def nombrado(nombre):
    return render_template('nombrado.html', nombre=nombre)

def ahora():
    ts = time.time()
    fecha_actual = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return fecha_actual

def guardar_fichero(nombre):
    f = open("registro.log", "a")
    f.write(ahora() + " " + nombre + "\n")

# Método HTTP POST
@app.post('/login')
def login_post():
    # return request.form
    nombre = request.form["nombre"]
    guardar_fichero(nombre)
    if nombre == "Pedro":
        return redirect(url_for("secreto"))
    else:
        return redirect(url_for("nombrado", nombre=nombre))

def buscar_fichero(needle):
    file = open("registro.log", "r")
    contador = 0
    for line in file:
        if needle in line:
            contador += 1
    return contador


@app.route('/info/<nombre>')
def info(nombre):
    return nombre + " Has entrado " + str(buscar_fichero(nombre)) + " veces."

    datos = request.get_json()
    usuario = datos.get('usuario') if datos else None
    return f'Se han añadido los datos del {usuario} correctamente'

@app.get('/')
def inicio():
    return render_template('index.html')



def current_user():
    return {'username': 'Oliver',
            'theme': 'patata',
            'image': 'manzanas'
            }

class User():
    def __init__(self, username, theme, image):
        self.username = username
        self.theme = theme
        self.image = image

    def a_dict(self):
        return {
            "username": self.username,
            "theme": self.theme,
            "image": url_for("static", filename=self.image),
        }

# Serializar
@app.route("/me")
def me_api():
    user = User('Oliver', 'patata', 'bob.jpg')
    texto_serializado = json.dumps(user.a_dict(), ensure_ascii=False)
    # return texto_serializado, 200, {'Content-Type': 'application/json'}
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("static", filename=user.image),
    }, 200, {'Content-Type': 'text/html'}




if __name__ == '__main__':
    app.run(debug=True)