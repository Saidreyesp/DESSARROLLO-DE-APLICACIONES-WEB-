from flask_login import UserMixin


class UsuarioLogin(UserMixin):
    """Adaptador de usuario para Flask-Login usando registros de MySQL."""

    def __init__(self, id_usuario, nombre, email, password):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @property
    def id(self):
        return str(self.id_usuario)

    @staticmethod
    def from_mysql_row(row):
        if not row:
            return None
        email = row.get('email') or row.get('mail')
        return UsuarioLogin(
            id_usuario=row.get('id_usuario'),
            nombre=row.get('nombre'),
            email=email,
            password=row.get('password'),
        )
