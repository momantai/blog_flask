import MySQLdb
datos=MySQLdb.connect("mysql2.paris1.alwaysdata.com","133991","momantai","momantaiter_blogflask")
conexion=datos.cursor()

def insertar():
    sql="INSERT INTO publicacion (cuerpo) VALUES ('adiis');"
    conexion.execute(sql)
    datos.commit()
