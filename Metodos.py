from flask import Flask, request, flash, redirect, url_for
from flask import render_template
from flask import session, escape
import time
import string
from flask_mysqldb import MySQL
import encriptacion
from flask_uploads import UploadSet, configure_uploads, IMAGES
photos = UploadSet('photos', IMAGES)


app= Flask(__name__)
app.secret_key = "super secret keyx"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "5fredy5"
app.config['MYSQL_DB'] = "momantaiter_blogflask"
mysql = MySQL(app)

#Configuración para cargar imagenes
app.config['UPLOADED_PHOTOS_DEST'] = "static/imagenes"
configure_uploads(app, photos)

#Función para encriptar
encriptar=encriptacion.encriptr


#Area de direcciones o URL----------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['POST', 'GET'])
def principal():
    conectar = mysql.connection.cursor()
    xy = ""
    #conectar.execute("SELECT * FROM Publicacion ORDER BY idPublicacion DESC limit 10")
    conectar.execute("""SELECT idPublicacion, titulo, cuerpo, portada,Nombre, Ape_pat, user, fechaPublicacion
        FROM Publicacion INNER JOIN momantaiter_blogflask.Usuario ON Usuario.idUsuario = Publicacion.Usuario_idUsuario
        INNER JOIN momantaiter_blogflask.Usuario_datos ON Usuario_datos.idUsuario_datos = Usuario.Usuario_datos_idUsuario_datos
        ORDER BY idPublicacion DESC limit 10""")
    resutado=conectar.fetchall()
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
    return render_template('Index.html',lista=resutado, sessionopen=xy)

#Ruta de direcciones para entrar al perfil de algún usuario con su nombre de usuario de manera "+nameUser"


@app.route('/<categoria>/<subcategoria>')
def categorias(categoria, subcategoria):
    conectar = mysql.connection.cursor()

    conectar.execute("""SELECT idPublicacion, titulo, cuerpo, portada,Nombre, Ape_pat, user, fechaPublicacion
        FROM Publicacion INNER JOIN momantaiter_blogflask.Usuario ON Usuario.idUsuario = Publicacion.Usuario_idUsuario
        INNER JOIN momantaiter_blogflask.Usuario_datos ON Usuario_datos.idUsuario_datos = Usuario.Usuario_datos_idUsuario_datos
        WHERE categoria = (%s) AND subCategoria = (%s) ORDER BY idPublicacion DESC""", [[categoria], [subcategoria]])

    resultado = conectar.fetchall()

    xy = ""
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
    return render_template("cat.html", sessionopen=xy, lista=resultado)

@app.route('/<categoria>')
def categoria(categoria):
    conectar = mysql.connection.cursor()

    conectar.execute("""SELECT idPublicacion, titulo, cuerpo, portada,Nombre, Ape_pat, user, fechaPublicacion
        FROM Publicacion INNER JOIN momantaiter_blogflask.Usuario ON Usuario.idUsuario = Publicacion.Usuario_idUsuario
        INNER JOIN momantaiter_blogflask.Usuario_datos ON Usuario_datos.idUsuario_datos = Usuario.Usuario_datos_idUsuario_datos
        WHERE categoria = (%s) ORDER BY idPublicacion DESC""", [categoria])

    resultado = conectar.fetchall()

    xy = ""
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
    return render_template("cat.html", sessionopen=xy, lista=resultado)

@app.route('/publicacion')
def publlicacion():
    conectar = mysql.connection.cursor()

    idpublicacion = request.args.get('ID')#se recibe el parametro de la url de index.html para hacer la consulta y mostrar el contenido en la ventana.
    conectar.execute("SELECT * FROM Publicacion WHERE idPublicacion = (%s)" % idpublicacion)
    resultado=conectar.fetchall()

    conectar.execute("SELECT Nombre, user, comentario FROM Comentario INNER JOIN Usuario ON Usuario.idUsuario = Comentario.Usuario_idUsuarioC INNER JOIN Usuario_datos ON Usuario_datos.idUsuario_datos = Usuario.Usuario_datos_idUsuario_datos WHERE Publicacion_idPublicacionC = (%s)" %idpublicacion)
    coments=conectar.fetchall()
    xy = ""
    if 'username' in session:
        xy = escape(session['username'])

    return render_template('Publicacion.html',resutado=resultado,comentarios=coments,id=idpublicacion, sessionopen=xy)

@app.route('/publicar', methods=['POST', 'GET'])
def publicar():
    conectar = mysql.connection.cursor()
    xy = ""
    if 'username' in session:
        xy = escape(session['username'])
        return render_template('publicar.html', sessionopen=xy)
    else:
        return redirect(url_for("login"))

@app.route('/editarPub')
def editarP():
    conectar = mysql.connection.cursor()
    idP = request.args.get('ref')
    if 'username' in session:
        i = escape(session['id'])
        conectar.execute("SELECT * FROM Publicacion WHERE idPublicacion = (%s) AND Usuario_idUsuario = (%s)", [[idP], [i]])
        publicacion = conectar.fetchall()
        print(publicacion)
        if len(publicacion) != 0:
            return render_template("modificarp.html", posteo = publicacion)
        else:
            return redirect("/")
@app.route('/edit', methods=['POST'])
def editP():
    conectar = mysql.connection.cursor()
    f = ""
    subCat = ""

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

    idU = escape(session['id'])
    try:
        f = photos.save(request.files['file'])

        conectar.execute("""UPDATE Publicacion SET titulo = (%s), cuerpo = (%s), categoria = (%s),
            subCategoria = (%s), portada = (%s) WHERE idPublicacion = (%s) and  Usuario_idUsuario = (%s)
            """, [[request.form['titulo']], [request.form['publicacion']], [request.form['categoria']], [subCat], [f], [request.form['xpubxid']], [idU]])
        mysql.connection.commit()
    except:
        conectar.execute("""UPDATE Publicacion SET titulo = (%s), cuerpo = (%s), categoria = (%s),
            subCategoria = (%s) WHERE idPublicacion = (%s) and  Usuario_idUsuario = (%s)
            """, [[request.form['titulo']], [request.form['publicacion']], [request.form['categoria']], [subCat], [request.form['xpubxid']], [idU]])
        mysql.connection.commit()
    return redirect("/publicacion?ID="+request.form['xpubxid'])


@app.route('/add', methods=['POST'])
def add_entry():
    conectar = mysql.connection.cursor()
    fecha=time.strftime("%y/%m/%d")
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

    #PD. Se agrego la categoria y subcategoria.
    conectar.execute("INSERT INTO Publicacion(titulo, cuerpo, categoria,fechaPublicacion, subCategoria,Usuario_idUsuario, portada) values(%s, %s, %s, %s, %s,%s,%s)", [request.form['titulo'], request.form['publicacion'], request.form['categoria'],fecha, subCat,session['id'], [f]])
    mysql.connection.commit()
    flash('Publicacion hecha')

    print(request.form['categoria'])
    print(subCat)

    return redirect(url_for('principal'))

@app.route('/deletePub')
def deletePub():
    conectar = mysql.connection.cursor()

    id = request.args.get('pub')
    conectar.execute("DELETE FROM Comentario WHERE Publicacion_idPublicacionC = (%s)", [id]);
    mysql.connection.commit()
    conectar.execute("DELETE FROM Publicacion WHERE idPublicacion = (%s)", [id]);
    mysql.connection.commit()

    return redirect("/")

@app.route('/addcoment', methods=['POST'])
def add_comentario():
    conectar = mysql.connection.cursor()
    fecha=time.strftime("%y/%m/%d")
    print(fecha)
    idpublicacion=request.args.get('ID')
    conectar.execute("""INSERT INTO Comentario(comentario,fechaComentario,Usuario_idUsuarioC,
        Publicacion_idPublicacionC)
        values (%s, %s,%s,%s)""",[request.form['comentario'],fecha,session['id'],idpublicacion])
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
    b = encriptar(request.form['passworde'])
    #Se conecta a la base de datos para verificar si el user y pass son correctos
    conectar.execute("SELECT idUsuario,user FROM Usuario WHERE user=(%s) and password=(%s) or correo=(%s) and password=(%s)", [a, b, a, b])
    respuesta = conectar.fetchone()

    if respuesta != None:
        #De ser así abre una nueva sesión.
        session['id']=respuesta[0]
        session['username'] = respuesta[1]
        return redirect(url_for("principal"))
    else:
        return loginOut()

@app.route('/logout')
def logout():
    #Elimina la sesion
    session.pop('username', None)
    session.pop('id')
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
    e = encriptar(request.form['contrasenia'])
    x = b.split(" ")

    conectar.execute("SELECT user FROM Usuario WHERE user=(%s) or idUsuario=(%s)", [c, d])
    respuesta = conectar.fetchone()



    if respuesta == None:
        conectar.execute("INSERT INTO Usuario_datos (idUsuario_datos,Nombre, Ape_pat, Ape_Mat, imagen_perfil, firma) VALUES (NULL, %s, %s, %s, 'defaultprofile.png','¡Soy nuevo aquí!');", [[a], [x[0]], [x[1]]])
        mysql.connection.commit()
        conectar.execute("SELECT MAX(idUsuario_datos) FROM Usuario_datos")
        idUsuario = conectar.fetchone()[0]
        print(idUsuario)
        conectar.execute("INSERT INTO Usuario VALUES (NULL, %s, %s, %s, %s);", [[c], [e], [idUsuario], [d]])
        mysql.connection.commit()
        return redirect("/login")
    else:
        print("Mal")
        return "<b>Usuario o correo ya en uso.</b>"

#Futura Area de Perfil de usuario :v

@app.route('/+<user>', methods=['POST', 'GET'])
def usuario(user):
    conectar = mysql.connection.cursor()

    #PD. Aun no hace nada por que aun se esta haciendo el html, pero ya se comprobo que funciona la url.
    conectar.execute("SELECT idUsuario,user,Nombre,Ape_pat,imagen_perfil,firma FROM  Usuario INNER JOIN  Usuario_datos ON  Usuario_datos_idUsuario_datos = idUsuario_datos  WHERE user =(%s);", [user])
    resultado = conectar.fetchall()

    conectar.execute("SELECT idPublicacion,portada,titulo,cuerpo,fechaPublicacion,user,Nombre,Ape_pat FROM  Usuario INNER JOIN Publicacion ON Usuario_idUsuario=idUsuario INNER JOIN  Usuario_datos ON  Usuario_datos_idUsuario_datos = idUsuario_datos  WHERE user =(%s);", [user])
    publicaciones = conectar.fetchall()
    xy = ""
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
        id=session['id']
        return render_template("user.html", sessionopen=xy, datos=resultado,publicaciones=publicaciones,id=id)
    else:
        return render_template("user.html", sessionopen=xy, datos=resultado,publicaciones=publicaciones)


@app.route('/Update-user')
def update():
    conectar = mysql.connection.cursor()
    if 'username' in session:
        conectar.execute("SELECT Nombre, Ape_pat, Ape_mat,idUsuario_datos FROM Usuario INNER JOIN Usuario_datos ON idUsuario_datos = Usuario_datos_idUsuario_datos WHERE idUsuario=(%s)",[session['id']])
        resutado=conectar.fetchall()
        return render_template("Actualizar_datos.html",resutado=resutado)
    else:
        return redirect("/login")
@app.route('/update-add', methods=['POST'])
def update_add():
    conectar = mysql.connection.cursor()
    id=request.args.get('code')
    nombre=request.form['nombre']
    apepat=request.form['ape_pat']
    apemat=request.form['ape_mat']
    conectar.execute("UPDATE Usuario_datos SET nombre=%s,Ape_pat=%s,Ape_mat=%s WHERE idUsuario_datos=%s",[ nombre,apepat ,apemat ,id])
    mysql.connection.commit()
    return redirect('/+%s' %session['username'])

#-------------------------------------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    app.run(debug=True, port=5000)
