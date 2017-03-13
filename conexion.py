import MySQLdb
datos=MySQLdb.connect("localhost","root","5fredy5","blog")
conexion=datos.cursor()

def insertar():
    sql="INSERT INTO publicacion (cuerpo) VALUES ('adiis');"
    conexion.execute(sql)
    datos.commit()

def imprecionparametros():
    sql="SELECT * FROM publicacion WHERE idpublicacion='3'"
    conexion.execute(sql)
    resutado=conexion.fetchall()
    for registro in resutado:
        idpublicacion=registro[0]
        cuerpo=registro[1]

    print(cuerpo)



imprecionparametros()
