from flask import Flask, request, jsonify, render_template
import os
import pymysql
import secrets
from pymysql import pooling

app = Flask(__name__)

# Configuración del pool de conexiones
def create_db_pool():
    return pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,  # Puedes ajustar el tamaño del pool según tus necesidades
        host='38.43.130.178',  # IP pública o nombre DNS de tu base de datos
        user='cliente',  # Usuario creado para conexiones remotas
        password='password',  # Contraseña del usuario
        database='bd_prueba',  # Nombre de tu base de datos
        port=3306,  # Puerto MySQL (3306 por defecto)
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ca': r'D:\project-folder\ca.pem'}  # Configuración de SSL para la conexión segura
    )

# Crear una instancia del pool de conexiones
connection_pool = create_db_pool()

def get_db_connection():
    # Obtener una conexión del pool
    return connection_pool.get_connection()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos JSON enviados desde el frontend
        credentials = request.get_json()  # Usar .get_json() para obtener el JSON

        if not credentials or 'username' not in credentials or 'password' not in credentials:
            return jsonify({"error": "Credenciales faltantes"}), 400

        username = credentials['username']
        password = credentials['password']

        try:
            connection = get_db_connection()

            # Validar las credenciales con la tabla 'usuarios' de la base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE user_ruc = %s AND password = %s", (username, password))
                result = cursor.fetchone()

            if result:
                # Si las credenciales son correctas, generar un token
                token = secrets.token_hex(16)  # Genera un token de 32 caracteres hexadecimales

                with connection.cursor() as cursor:
                    # Insertar o actualizar el token en la tabla 'tokens'
                    cursor.execute(""" 
                        INSERT INTO tokens (token, user_ruc, created_at)
                        VALUES (%s, %s, NOW())
                        ON DUPLICATE KEY UPDATE token = VALUES(token), created_at = NOW();
                    """, (token, username))
                    connection.commit()

                return jsonify({"token": token})  # Retorna el token como respuesta

            else:
                return jsonify({"error": "Credenciales inválidas"}), 401

        except Exception as e:
            return jsonify({"error": f"Error en la base de datos: {str(e)}"}), 500
        finally:
            connection.close()

    return render_template('login.html')  # Si es un GET, renderiza el formulario de login

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    # Si es un GET, muestra la página para ingresar el RUC
    return render_template('consulta.html')

@app.route('/ruc-info', methods=['GET', 'POST'])
def ruc_info():
    if request.method == 'POST':
        # Solicitud para consultar la información del RUC
        ruc = request.json.get('ruc')  # Asegúrate de que estamos usando JSON y no 'form'
        token = request.headers.get('Authorization').split(" ")[1]  # Obtener el token del encabezado

        try:
            connection = get_db_connection()

            # Verificar si el token es válido
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_ruc FROM tokens WHERE token = %s", (token,))
                result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Token inválido"}), 403

            user_ruc = result['user_ruc']  # Obtener el RUC asociado al token

            # Realizar la consulta usando el RUC
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM padron_reducido_ruc WHERE RUC = %s", (ruc,))
                ruc_data = cursor.fetchone()

            if ruc_data:
                return jsonify(ruc_data)  # Retornar datos como JSON
            else:
                return jsonify({"error": "RUC no encontrado"}), 404

        except Exception as e:
            return jsonify({"error": f"Error al procesar la solicitud: {e}"}), 500
        finally:
            connection.close()

    elif request.method == 'GET':
        # Solicitud para mostrar la información del RUC desde la URL
        ruc = request.args.get('ruc')

        try:
            connection = get_db_connection()

            # Realizar la consulta usando el RUC
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM padron_reducido_ruc WHERE RUC = %s", (ruc,))
                ruc_data = cursor.fetchone()

            if ruc_data:
                return render_template('ruc-info.html', ruc_data=ruc_data)
            else:
                return render_template('ruc-info.html', error="RUC no encontrado")

        except Exception as e:
            return render_template('ruc-info.html', error=f"Error al procesar la solicitud: {e}")
        finally:
            connection.close()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Heroku asigna un puerto dinámico
    app.run(debug=True, host='0.0.0.0', port=port)
