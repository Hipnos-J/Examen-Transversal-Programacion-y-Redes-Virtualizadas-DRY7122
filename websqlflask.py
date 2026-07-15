from flask import Flask, request, render_template_string
import sqlite3
import hashlib

app = Flask(__name__)
DB_NAME = "usuarios_examen.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
                 (USERNAME TEXT PRIMARY KEY NOT NULL, HASH TEXT NOT NULL);''')
    conn.commit()
   
    integrantes = ["Josue Jorquera", "Otro Integrante"]
    password_defecto = "Cisco123!"
    hash_value = hashlib.sha256(password_defecto.encode()).hexdigest()
   
    for integrante in integrantes:
        try:
            c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES ('{0}', '{1}')".format(integrante, hash_value))
        except sqlite3.IntegrityError:
            pass 
    conn.commit()
    conn.close()

HTML_LOGIN = '''
<!DOCTYPE html>
<html>
<head><title>Examen DRY7122</title></head>
<body>
    <h2>Login Examen Transversal</h2>
    <form method="POST" action="/login">
        Username (Nombre Integrante): <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Ingresar">
    </form>
    <p style="color:red;">{{ error }}</p>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_LOGIN, error="")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].lower().strip()
    password = request.form['password']
   
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username))
    record = c.fetchone()
    conn.close()
   
    if not record:
        return render_template_string(HTML_LOGIN, error="Usuario no corresponde a un integrante del examen.")
   
    # Validar Hash
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    if record[0] == input_hash:
        return f"<h1>Bienvenido(a) {username.upper()}. Autenticación Exitosa (Hash Correcto).</h1>"
    else:
        return render_template_string(HTML_LOGIN, error="Contraseña incorrecta.")

if __name__ == '__main__':
    init_db()
    print("Base de datos lista. Iniciando servidor en puerto 5800...")
    app.run(host='0.0.0.0', port=5800)