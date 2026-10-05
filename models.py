from flask_login import UserMixin
from conexion.conexion import get_db


class User(UserMixin):
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.username = data["username"]
        self.password = data["password"]
        self.email = data["email"]
        self.rol = data["rol"]

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id=%s", (user_id,))
            data = cursor.fetchone()
        return User(data) if data else None

    @staticmethod
    def get_by_username(username):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
            data = cursor.fetchone()
        return User(data) if data else None


class Idea:
    @staticmethod
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, u.nombre AS creador
                FROM productos p
                LEFT JOIN usuarios u ON p.usuario_id = u.id
                ORDER BY p.fecha_creacion DESC
            """)
            return cursor.fetchall()

    @staticmethod
    def get_by_id(idea_id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE id=%s", (idea_id,))
            return cursor.fetchone()

    @staticmethod
    def get_recent(limit=5):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, u.nombre AS creador
                FROM productos p
                LEFT JOIN usuarios u ON p.usuario_id = u.id
                ORDER BY p.fecha_creacion DESC
                LIMIT %s
            """, (limit,))
            return cursor.fetchall()

    @staticmethod
    def count_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM productos")
            return cursor.fetchone()["total"]


class Cliente:
    @staticmethod
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes ORDER BY nombre")
            return cursor.fetchall()

    @staticmethod
    def count_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM clientes")
            return cursor.fetchone()["total"]


class Proveedor:
    @staticmethod
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM proveedores ORDER BY nombre")
            return cursor.fetchall()

    @staticmethod
    def count_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM proveedores")
            return cursor.fetchone()["total"]


class Factura:
    @staticmethod
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT f.*, c.nombre AS cliente
                FROM facturacion f
                INNER JOIN clientes c ON f.cliente_id = c.id
                ORDER BY f.fecha DESC
            """)
            return cursor.fetchall()

    @staticmethod
    def count_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM facturacion")
            return cursor.fetchone()["total"]
