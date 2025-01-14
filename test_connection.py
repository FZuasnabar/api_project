import pymysql

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='password',
        database='bd_prueba'
    )
    print("Conexión exitosa")
except Exception as e:
    print(f"Error de conexión: {e}")
finally:
    if connection:
        connection.close()
