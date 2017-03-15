import conexion
from flask import Flask, request, flash, redirect, url_for
from flask import render_template


app= Flask(__name__)
app.secret_key = "super secret key"
conectar=conexion.conexion

@app.route('/', methods=['POST', 'GET'])
def principal():
    conectar.execute("SELECT * FROM publicacion")
    resutado=conectar.fetchall()
    return render_template('Index.html',lista=resutado)

@app.route('/publicacion')
def publlicacion():
	return render_template('Publicacion.html')

@app.route('/publicar', methods=['POST', 'GET'])
def publica():
	return render_template('publicar.html')

@app.route('/add', methods=['POST'])
def add_entry():
    conectar.execute("INSERT INTO publicacion(titulo, cuerpo) values(%s, %s)", [request.form['titulo'], request.form['cuerpo']])
    conexion.datos.commit()
    flash('Publicacion hecha')
    return redirect(url_for('principal'))

if __name__=='__main__':
    app.run(debug=True, port=5000)
