from flask import Flask, render_template
import psycopg2
from flask import jsonify
import bcrypt

app = Flask(__name__)

app.secret_key = "impossible"

import psycopg2

#'''def get_db_connection():
#    return psycopg2.connect(
#        host="localhost",
#        database="bdloa",
#        user="postgres",
#        password="1234"
#    )'''
def get_db_connection():
    return psycopg2.connect(
        os.environ.get("postgresql://bdloa_user:8fLDqwmSxOfy8bs6SylMkrXqrZBHg5rx@dpg-d79bjmnfte5s739jkf1g-a/bdloa"),
        sslmode="require"
    )
 

@app.route('/')
def home():
    return render_template('index.html')

from flask import session

@app.route('/login', methods=['POST'])
def login():

    usuario = request.form['usuario']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT idusuario, password, rol
        FROM tusuario00
        WHERE usuario = %s AND estado = 'A'
    """, (usuario,))

    user = cur.fetchone()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        session['idusuario'] = user[0]
        session['rol'] = user[2]
        return redirect('/')

    cur.close()
    conn.close()

    if user:
        session['idusuario'] = user[0]
        session['rol'] = user[1]

        return redirect('/')

    return "ERROR: Credenciales incorrectas"

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/departamentos')
def departamentos():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, nombre FROM departamento")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(data)

@app.route('/provincias/<int:dep_id>')
def provincias(dep_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, nombre FROM provincia WHERE departamento_id = %s", (dep_id,))
    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(data)

@app.route('/distritos/<int:prov_id>')
def distritos(prov_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, nombre FROM distrito WHERE provincia_id = %s", (prov_id,))
    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(data)

from flask import request, redirect

@app.route('/guardar_cliente', methods=['POST'])
def guardar_cliente():

    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    dni = request.form['dni']
    correo = request.form['correo']
    celular = request.form['celular']
    direccion = request.form['direccion']

    departamento_id = request.form['departamento_id']
    provincia_id = request.form['provincia_id']
    distrito_id = request.form['distrito_id']

    usuario = "web"

    conn = get_db_connection()
    cur = conn.cursor()

    # 🔥 VALIDAR DUPLICADOS
    cur.execute("""
        SELECT 1 FROM tcliente00
        WHERE dni = %s OR correo = %s OR celular = %s
    """, (dni, correo, celular))

    existe = cur.fetchone()

    if existe:
        cur.close()
        conn.close()
        return "ERROR: Cliente ya registrado (Datos de DNI, correo o celular duplicado)"

    # INSERT
    cur.execute("""
        INSERT INTO tcliente00
        (nombre, apellidos, dni, correo, celular, direccion,
         departamento_id, provincia_id, distrito_id, usuario)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_cliente
    """, (
        nombre, apellidos, dni, correo, celular, direccion,
        departamento_id, provincia_id, distrito_id,
        usuario
    ))

    idcliente = cur.fetchone()[0]
    
    # Crear registro inicial en tplaxcli00 (sin plan aún)
    cur.execute("""
        INSERT INTO tplaxcli00 (idcliente, codplan, estado, usuario, fcreacion)
        VALUES (%s, NULL, 'N', %s, NOW())
    """, (idcliente, usuario))

    conn.commit()
    cur.close()
    conn.close()

    return render_template('planes.html', idcliente=idcliente)

@app.route('/seleccionar_plan', methods=['POST'])
def seleccionar_plan():

    idcliente = request.form['idcliente']
    plan = request.form['plan']

    conn = get_db_connection()
    cur = conn.cursor()

    # Verificar si ya existe
    cur.execute("""
        SELECT idplacli 
        FROM tplaxcli00 
        WHERE idcliente = %s
        ORDER BY idplacli DESC
        LIMIT 1
    """, (idcliente,))

    existe = cur.fetchone()

    if existe:
        # 🔄 UPDATE
        cur.execute("""
            UPDATE tplaxcli00
            SET codplan = %s,
                estado = 'N',
                fmodificacion = NOW(),
                usuario = %s
            WHERE idplacli = %s
        """, (plan, 'web', existe[0]))

    else:
        # 🆕 INSERT
        cur.execute("""
            INSERT INTO tplaxcli00 (idcliente, codplan, usuario, estado, fcreacion)
            VALUES (%s, %s, %s, 'N', NOW())
        """, (idcliente, plan, 'web'))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/pago')

@app.route('/pago')
def pago():

    # ejemplo simple (luego lo haremos dinámico)
    return render_template('pago.html',
                           plan="PLAN HOGAR",
                           precio="44")
 
    
@app.route('/clientes')
def clientes():

    conn = get_db_connection()
    cur = conn.cursor()
    
    estado = (request.args.get('estado') or "").strip()

    # 🔹 CLIENTES
    if estado.lower() == "todos":
        cur.execute("""
        SELECT 
            c.id_cliente,
            c.nombre,
            c.apellidos,
            c.dni,
            c.correo,
            c.celular,
            c.direccion,

            d.nombre as departamento,
            p.nombre as provincia,
            di.nombre as distrito,

            pl.codplan,
            pl.estado,
            c.usuario

        FROM tcliente00 c

        LEFT JOIN tplaxcli00 pl ON c.id_cliente = pl.idcliente
        LEFT JOIN departamento d ON c.departamento_id = d.id
        LEFT JOIN provincia p ON c.provincia_id = p.id
        LEFT JOIN distrito di ON c.distrito_id = di.id

        ORDER BY c.id_cliente DESC
        LIMIT 200
    """)
    else:
        cur.execute("""
            SELECT 
                c.id_cliente,
                c.nombre,
                c.apellidos,
                c.dni,
                c.correo,
                c.celular,
                c.direccion,

                d.nombre as departamento,
                p.nombre as provincia,
                di.nombre as distrito,

                pl.codplan,
                te.destado,
                c.usuario

            FROM tcliente00 c

            LEFT JOIN tplaxcli00 pl ON c.id_cliente = pl.idcliente
            LEFT JOIN departamento d ON c.departamento_id = d.id
            LEFT JOIN provincia p ON c.provincia_id = p.id
            LEFT JOIN distrito di ON c.distrito_id = di.id
            LEFT JOIN testado00 te ON te.cestado=pl.estado

            ORDER BY c.id_cliente DESC
        """)

    data = cur.fetchall()

    # 🔹 ESTADOS (NUEVO)
    cur.execute("""
        SELECT cestado, destado
        FROM testado00
        WHERE estado = 'N'
        ORDER BY idestado
    """)

    estados = cur.fetchall()
    
    print("ESTADOS:", estados)

    cur.close()
    conn.close()
    
   

    return render_template('clientes.html', clientes=data, estados=estados)
    
@app.route('/pago_exito')
def pago_exito():

    conn = get_db_connection()
    cur = conn.cursor()

    # 🔥 SOLO el último registro del cliente
    cur.execute("""
        UPDATE tplaxcli00
        SET estado = 'C',
            fmodificacion = CURRENT_TIMESTAMP
        WHERE idplacli = (
            SELECT MAX(idplacli) FROM tplaxcli00
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

    return render_template('pago_exito.html',
                           plan="PLAN HOGAR",
                           precio="44")
    
@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():

    dni = request.form['dni']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    correo = request.form['correo']
    celular = request.form['celular']

    usuario = request.form['usuario']
    

    password = request.form['password'].encode('utf-8')
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    direccion = request.form['direccion']
    
    def to_int(value):
        return int(value) if value else None
    
    departamento_id = to_int(request.form.get('departamento_id'))
    provincia_id = to_int(request.form.get('provincia_id'))
    distrito_id = to_int(request.form.get('distrito_id'))
    
    conn = get_db_connection()
    cur = conn.cursor()

    # 🔐 VALIDAR USUARIO DUPLICADO
    # Usuario
    cur.execute("SELECT 1 FROM tusuario00 WHERE usuario = %s", (usuario,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return "ERROR: Ya existe un usuario con ese USUARIO"

    # DNI
    cur.execute("SELECT 1 FROM tusuario00 WHERE dni = %s", (dni,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return "ERROR: Ya existe un usuario con ese DNI"

    # Correo
    cur.execute("SELECT 1 FROM tusuario00 WHERE correo = %s", (correo,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return "ERROR: Ya existe un usuario con ese CORREO"

    # Celular
    cur.execute("SELECT 1 FROM tusuario00 WHERE celular = %s", (celular,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return "ERROR: Ya existe un usuario con ese CELULAR"

    # 🆕 INSERT
    cur.execute("""
        INSERT INTO tusuario00
        (dni, nombre, apellidos, correo, celular,
         usuario, password, direccion,
         departamento_id, provincia_id, distrito_id,
         rol, fcreacion, fmodificacion, estado)
        VALUES (%s,%s,%s,%s,%s,
                %s,%s,%s,
                %s,%s,%s,
                'Usuario', NOW(), NOW(), 'A')
    """, (
        dni, nombre, apellidos, correo, celular,
        usuario, password_hash, direccion,
        departamento_id, provincia_id, distrito_id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')  # vuelve al inicio

if __name__ == '__main__':
    app.run(debug=True)
