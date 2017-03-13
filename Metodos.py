import conexion
from flask import Flask
from flask import render_template


app= Flask(__name__)

@app.route('/')
def principal():
    conectar=conexion.conexion
    sql="SELECT * FROM publicacion"
    conectar.execute(sql)
    resutado=conectar.fetchall()
    lista=[]
    for registro in resutado:
       idpublicacion=registro[0]
       cuerpo=registro[1]
       lista.append(cuerpo)
    return render_template('Index.html',lista=lista)

@app.route('/publicacion')
def publlicacion():
	return render_template('Publicacion.html')

if __name__=='__main__':
    app.run(debug=True, port=5000)
