#import conexion
from flask import Flask, request, flash, redirect, url_for
from flask import render_template
from flask import session, escape

from flask_mysqldb import MySQL

from flask_uploads import UploadSet, configure_uploads, IMAGES
photos = UploadSet('photos', IMAGES)


app= Flask(__name__)
app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = "mysql2.paris1.alwaysdata.com"
app.config['MYSQL_USER'] = "133991"
app.config['MYSQL_PASSWORD'] = "momantai"
app.config['MYSQL_DB'] = "momantaiter_blogflask"

mysql = MySQL(app)

#Configuración para cargar imagenes
app.config['UPLOADED_PHOTOS_DEST'] = "static/imagenes"
configure_uploads(app, photos)


#Area de direcciones o URL----------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['POST', 'GET'])
def principal():
    conectar = mysql.connection.cursor()
    
    xy = ""
    conectar.execute("SELECT * FROM publicacion ORDER BY id DESC limit 10")
    resutado=conectar.fetchall()
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
    return render_template('Index.html',lista=resutado, sessionopen=xy)

#Ruta de direcciones para entrar al perfil de algún usuario con su nombre de usuario de manera "+nameUser"
@app.route('/+<user>', methods=['POST', 'GET'])
def usuario(user):
    conectar = mysql.connection.cursor()

    #PD. Aun no hace nada por que aun se esta haciendo el html, pero ya se comprobo que funciona la url.
    conectar.execute("SELECT idUser, user, correo FROM users WHERE user = (%s);", [user])
    resultado = conectar.fetchall()

    xy = ""
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])

    return render_template("user.html", sessionopen=xy)

@app.route('/<categoria>/<subcategoria>')
def categorias(categoria, subcategoria):
    conectar = mysql.connection.cursor()

    conectar.execute("SELECT * FROM publicacion WHERE Categoria = (%s) and SubCategoria = (%s);", [[categoria], [subcategoria]])
    resultado = conectar.fetchall()

    xy = ""
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
    return render_template("cat.html", sessionopen=xy, lista=resultado)

@app.route('/<categoria>')
def categoria(categoria):
    conectar = mysql.connection.cursor()

    conectar.execute("SELECT * FROM publicacion WHERE Categoria = (%s);", [categoria])
    resultado = conectar.fetchall()

    xy = ""
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
    return render_template("cat.html", sessionopen=xy, lista=resultado)

@app.route('/publicacion')
def publlicacion():
    conectar = mysql.connection.cursor()

    idpublicacion = request.args.get('ID')#se recibe el parametro de la url de index.html para hacer la consulta y mostrar el contenido en la ventana.
    conectar.execute("SELECT * FROM publicacion WHERE id=(%s)" % idpublicacion)
    resultado=conectar.fetchall()

    conectar.execute("SELECT * FROM comentarios WHERE idpublicacion=(%s)" %idpublicacion)
    coments=conectar.fetchall()
    xy = ""
    if 'username' in session:
        xy = escape(session['username'])

    return render_template('Publicacion.html',resutado=resultado,comentarios=coments,id=idpublicacion, sessionopen=xy)

@app.route('/publicar', methods=['POST', 'GET'])
def publica():
    conectar = mysql.connection.cursor()

    xy = ""
    if 'username' in session:
        xy = escape(session['username'])
        return render_template('publicar.html', sessionopen=xy)
    else:
        return redirect(url_for("login"))


@app.route('/add', methods=['POST'])
def add_entry():
    conectar = mysql.connection.cursor()

    #Aquí obtenemos el archivo por metodo POST y es almacenado en la carpeta configurada para almacenar las imagenes.
    #También recogemos el valor de la ruta para ser alcacenada en base de datos.
    f = photos.save(request.files['file'])

    subCat = ""
    #HUbo un probema con la elección de las subcategorias que fue resulto de esta manera if-else
    if request.form["categoria"]=="1":
        subCat = request.form['cat1']
    elif request.form["categoria"]=="2":
        subCat = request.form['cat2']
    elif request.form["categoria"]=="3":
        subCat = request.form['cat3']
    elif request.form["categoria"]=="4":
        subCat = request.form['cat4']
    elif request.form["categoria"]=="5":
        subCat = request.form['cat5']
    else:
        subCat = ""

    print(request.form['categoria'])
    print(subCat)

    #PD. Se agrego la categoria y subcategoria.
    conectar.execute("INSERT INTO publicacion(titulo, cuerpo, Categoria, SubCategoria, portada) values(%s, %s, %s, %s, %s)", [request.form['titulo'], request.form['publicacion'], request.form['categoria'], subCat, [f]])
    mysql.connection.commit()
    flash('Publicacion hecha')

    print(request.form['categoria'])
    print(subCat)

    return redirect(url_for('principal'))

@app.route('/deletePub')
def deletePub():
    conectar = mysql.connection.cursor()

    id = request.args.get('pub')
    conectar.execute("DELETE FROM comentarios WHERE idPublicacion = (%s)", [id]);
    mysql.connection.commit()
    conectar.execute("DELETE FROM publicacion WHERE id = (%s)", [id]);
    mysql.connection.commit()

    return redirect("/")

@app.route('/addcoment', methods=['POST'])
def add_comentario():
    conectar = mysql.connection.cursor()

    idpublicacion=request.args.get('ID')
    conectar.execute("INSERT INTO comentarios(comentario,idpublicacion) values (%s, %s)",[request.form['comentario'],idpublicacion])
    mysql.connection.commit()
    return redirect("/publicacion?ID=%s" %idpublicacion)


#Area del login y registro ------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for("principal"))
    return render_template('login.html')
def loginOut():
    return render_template('login.html', xerror=True)

def a():
    return "Hola"

@app.route('/loginIn', methods=['POST'])
def loginIn():
    conectar = mysql.connection.cursor()

    verr = 0
    #Obtiene los datos enviados desde el formulario de login.
    a = request.form['username']
    b = request.form['passworde']
    #Se conecta a la base de datos para verificar si el user y pass son correctos
    conectar.execute("SELECT user FROM users WHERE user=(%s) and contrasenia=(%s) or correo=(%s) and contrasenia=(%s)", [a, b, a, b])
    respuesta = conectar.fetchone()

    if respuesta != None:
        #De ser así abre una nueva sesión.
        session['username'] = respuesta[0]
        return redirect(url_for("principal"))
    else:
        return loginOut()

@app.route('/logout')
def logout():
    #Elimina la sesion
    session.pop('username', None)
    return redirect(url_for("principal"))


#Area de registro
@app.route('/register')
def registrar():
    return render_template('registrar.html')

@app.route('/registerOn', methods=['POST'])
def registrarOn():
    conectar = mysql.connection.cursor()

    a = request.form['nombre']
    b = request.form['apellido']
    c = request.form['usuario']
    d = request.form['correo']
    e = request.form['contrasenia']

    conectar.execute("SELECT user FROM users WHERE user=(%s) or correo=(%s)", [c, d])
    respuesta = conectar.fetchone()

    if respuesta == None:
        print("Bien")
        return "<b>bien</b>"
    else:
        print("Mal")
        return "<b>mal</b>"

#Futura Area de Perfil de usuario :v

#-------------------------------------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    app.run(debug=True, port=5000)
