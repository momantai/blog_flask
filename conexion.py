import MySQLdb
datos=MySQLdb.connect("localhost","root","5fredy5","blog")
conexion=datos.cursor()

def insertar():
    sql="INSERT INTO publicacion (cuerpo) VALUES ('adiis');"
    conexion.execute(sql)
    datos.commit()
