import conexion
from flask import Flask, request, flash, redirect, url_for
from flask import render_template


app= Flask(__name__)
app.secret_key = "super secret key"
conectar=conexion.conexion

@app.route('/', methods=['POST', 'GET'])
def principal():
    conectar.execute("SELECT * FROM publicacion ORDER BY id DESC limit 10")
    resutado=conectar.fetchall()
    return render_template('Index.html',lista=resutado)

@app.route('/publicacion')
def publlicacion():
    idpublicacion = request.args.get('ID')#se recibe el parametro de la url de index.html para hacer la consulta y mostrar el contenido en la ventana.
    conectar.execute("SELECT * FROM publicacion WHERE id=(%s)" % idpublicacion)
    resultado=conectar.fetchall()

    conectar.execute("SELECT * FROM comentarios WHERE idpublicacion=(%s)" %idpublicacion)
    coments=conectar.fetchall()
    return render_template('Publicacion.html',resutado=resultado,comentarios=coments,id=idpublicacion)

@app.route('/publicar', methods=['POST', 'GET'])
def publica():
	return render_template('publicar.html')

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
