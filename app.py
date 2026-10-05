from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from uuid import uuid4

from conexion.conexion import get_db, close_db
from models import User, Idea, Cliente, Proveedor, Factura
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esta-clave-en-produccion"

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta sección."


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db(exception)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data.strip())
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Inicio de sesión correcto.", "success")
            return redirect(url_for("dashboard"))
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html", form=form)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = UsuarioForm()
    if form.validate_on_submit():
        if User.get_by_username(form.username.data.strip()):
            flash("El nombre de usuario ya existe.", "danger")
        else:
            user_id = str(uuid4())
            password_hash = generate_password_hash(form.password.data)
            db = get_db()
            with db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO usuarios (id, nombre, username, password, email, rol)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        user_id,
                        form.nombre.data.strip(),
                        form.username.data.strip(),
                        password_hash,
                        form.email.data.strip(),
                        form.rol.data,
                    ),
                )
            db.commit()
            flash("Usuario registrado correctamente. Ya puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

    return render_template("registro.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        total_ideas=Idea.count_all(),
        total_clientes=Cliente.count_all(),
        total_proveedores=Proveedor.count_all(),
        total_facturas=Factura.count_all(),
        ideas_recientes=Idea.get_recent(5),
    )


@app.route("/productos")
@login_required
def productos():
    return render_template("productos.html", productos=Idea.get_all())


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO productos
                (id, nombre, descripcion, categoria, estado, usuario_id, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(uuid4()),
                    form.nombre.data.strip(),
                    form.descripcion.data.strip(),
                    form.categoria.data,
                    form.estado.data,
                    current_user.id,
                    datetime.now(),
                ),
            )
        db.commit()
        flash("Idea registrada correctamente.", "success")
        return redirect(url_for("productos"))

    return render_template("formulario_producto.html", form=form, titulo="Registrar idea")


@app.route("/productos/editar/<producto_id>", methods=["GET", "POST"])
@login_required
def editar_producto(producto_id):
    producto = Idea.get_by_id(producto_id)
    if not producto:
        flash("La idea no existe.", "danger")
        return redirect(url_for("productos"))

    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE productos
                SET nombre=%s, descripcion=%s, categoria=%s, estado=%s
                WHERE id=%s
                """,
                (
                    form.nombre.data.strip(),
                    form.descripcion.data.strip(),
                    form.categoria.data,
                    form.estado.data,
                    producto_id,
                ),
            )
        db.commit()
        flash("Idea actualizada correctamente.", "success")
        return redirect(url_for("productos"))

    return render_template("formulario_producto.html", form=form, titulo="Editar idea")


@app.route("/productos/eliminar/<producto_id>", methods=["POST"])
@login_required
def eliminar_producto(producto_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM productos WHERE id=%s", (producto_id,))
    db.commit()
    flash("Idea eliminada correctamente.", "success")
    return redirect(url_for("productos"))


@app.route("/clientes")
@login_required
def clientes():
    return render_template("clientes.html", clientes=Cliente.get_all())


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO clientes
                (id, nombre, empresa, email, telefono, fecha_registro)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    str(uuid4()),
                    form.nombre.data.strip(),
                    form.empresa.data.strip(),
                    form.email.data.strip(),
                    form.telefono.data.strip(),
                    datetime.now(),
                ),
            )
        db.commit()
        flash("Cliente registrado correctamente.", "success")
        return redirect(url_for("clientes"))
    return render_template("clientes.html", clientes=Cliente.get_all(), form=form, mostrar_form=True)


@app.route("/proveedores")
@login_required
def proveedores():
    return render_template("proveedores.html", proveedores=Proveedor.get_all())


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO proveedores
                (id, nombre, servicio, email, telefono)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    str(uuid4()),
                    form.nombre.data.strip(),
                    form.servicio.data.strip(),
                    form.email.data.strip(),
                    form.telefono.data.strip(),
                ),
            )
        db.commit()
        flash("Proveedor registrado correctamente.", "success")
        return redirect(url_for("proveedores"))
    return render_template("proveedores.html", proveedores=Proveedor.get_all(), form=form, mostrar_form=True)


@app.route("/facturacion")
@login_required
def facturacion():
    return render_template("facturacion.html", facturas=Factura.get_all(), clientes=Cliente.get_all())


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():
    form = FacturacionForm()
    form.cliente_id.choices = [(c["id"], c["nombre"]) for c in Cliente.get_all()]

    if form.validate_on_submit():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO facturacion
                (id, cliente_id, concepto, monto, estado, fecha)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    str(uuid4()),
                    form.cliente_id.data,
                    form.concepto.data.strip(),
                    form.monto.data,
                    form.estado.data,
                    datetime.now(),
                ),
            )
        db.commit()
        flash("Factura registrada correctamente.", "success")
        return redirect(url_for("facturacion"))

    return render_template("facturacion.html", facturas=Factura.get_all(), clientes=Cliente.get_all(), form=form, mostrar_form=True)


if __name__ == "__main__":
    app.run(debug=True)
