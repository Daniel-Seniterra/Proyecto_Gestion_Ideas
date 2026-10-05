from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ClienteForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=3, max=120)])
    empresa = StringField("Empresa", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Correo", validators=[DataRequired(), Email(), Length(max=120)])
    telefono = StringField("Teléfono", validators=[DataRequired(), Length(min=7, max=30)])
    submit = SubmitField("Guardar cliente")
