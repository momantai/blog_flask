import conexion
from flask import Flask
from flask import render_template


app= Flask(__name__)

@app.route('/')
def principal():
    conectar=conexion.conexion
    conectar.execute("SELECT * FROM publicacion")
    resutado=conectar.fetchall()
    
    return render_template('Index.html',lista=resutado)

@app.route('/publicacion')
def publlicacion():
	return render_template('Publicacion.html')

if __name__=='__main__':
    app.run(debug=False, port=5000)
