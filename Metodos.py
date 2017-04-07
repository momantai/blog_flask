import conexion
from flask import Flask, request, flash, redirect, url_for
from flask import render_template
from flask import session, escape


app= Flask(__name__)
app.secret_key = "super secret key"
conectar=conexion.conexion

@app.route('/', methods=['POST', 'GET'])
def principal():
    xy = ""
    conectar.execute("SELECT * FROM publicacion ORDER BY id DESC limit 10")
    resutado=conectar.fetchall()
    if 'username' in session: #Verifica si hay un usuario en sesion
        xy = escape(session['username'])
    return render_template('Index.html',lista=resutado, sessionopen=xy)




@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for("principal"))
    return render_template('login.html')
@app.route('/logout')
def logout():
    #Elimina la sesion
    session.pop('username', None)
    return redirect(url_for("principal"))

@app.route('/loginIn', methods=['POST'])
def loginIn():
    verr = 0
    #Obtiene los datos enviados desde el formulario de login.
    a = request.form['username']
    b = request.form['passworde']
    #Se conecta a la base de datos para verificar si el user y pass son correctos
    conectar.execute("SELECT user FROM users WHERE user=(%s) or correo=(%s) and contrasenia=(%s)", [a, a, b])
    respuesta = conectar.fetchone()

    for i in respuesta:
        verr = 1

    if verr == 1:
        #De ser así abre una nueva sesión.
        session['username'] = respuesta[0]
        return redirect(url_for("principal"))
    else:
        return "n"




@app.route('/publicacion')
def publlicacion():
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
    xy = ""
    if 'username' in session:
        xy = escape(session['username'])
        return render_template('publicar.html', sessionopen=xy)
    else:
        return redirect(url_for("login"))
    

@app.route('/add', methods=['POST'])
def add_entry():
    conectar.execute("INSERT INTO publicacion(titulo, cuerpo, Categoria, SubCategoria) values(%s, %s, 'computador', 'programas')", [request.form['titulo'], request.form['publicacion']])
    conexion.datos.commit()
    flash('Publicacion hecha')
    return redirect(url_for('principal'))

@app.route('/addcoment', methods=['POST'])
def add_comentario():
    idpublicacion=request.args.get('ID')
    conectar.execute("INSERT INTO comentarios(comentario,idpublicacion) values (%s, %s)",[request.form['comentario'],idpublicacion])
    conexion.datos.commit()
    return redirect("/publicacion?ID=%s" %idpublicacion)

if __name__=='__main__':
    app.run(debug=True, port=5000)
