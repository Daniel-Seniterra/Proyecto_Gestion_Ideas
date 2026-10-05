from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class UsuarioForm(FlaskForm):
    nombre = StringField(
        "Nombre completo",
        validators=[DataRequired(), Length(min=3, max=100)]
    )
    username = StringField(
        "Nombre de usuario",
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    email = StringField(
        "Correo electrónico",
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=6, max=100)]
    )
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden.")]
    )
    rol = SelectField(
        "Rol",
        choices=[
            ("usuario", "Usuario"),
            ("administrador", "Administrador")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Registrarse")
