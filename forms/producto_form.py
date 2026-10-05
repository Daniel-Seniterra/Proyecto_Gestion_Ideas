from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductoForm(FlaskForm):
    nombre = StringField(
        "Nombre de la idea",
        validators=[DataRequired(), Length(min=3, max=150)]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(), Length(min=10, max=1000)]
    )
    categoria = SelectField(
        "Categoría",
        choices=[
            ("Tecnología", "Tecnología"),
            ("Educación", "Educación"),
            ("Negocios", "Negocios"),
            ("Innovación", "Innovación"),
            ("Medio ambiente", "Medio ambiente"),
            ("Otro", "Otro")
        ],
        validators=[DataRequired()]
    )
    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("En análisis", "En análisis"),
            ("Aprobada", "Aprobada"),
            ("Rechazada", "Rechazada")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Guardar idea")
