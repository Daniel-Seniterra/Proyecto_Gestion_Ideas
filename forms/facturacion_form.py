from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):
    cliente_id = SelectField("Cliente", validators=[DataRequired()], coerce=str)
    concepto = StringField("Concepto", validators=[DataRequired(), Length(min=3, max=200)])
    monto = DecimalField(
        "Monto",
        validators=[DataRequired(), NumberRange(min=0)]
    )
    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Pagada", "Pagada"),
            ("Anulada", "Anulada")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Registrar factura")
