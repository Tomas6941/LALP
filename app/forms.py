from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired, Length

TIPOS = [("sugerencia", "Sugerencia"), ("reclamo", "Reclamo"), ("idea", "Idea")]


class ContactForm(FlaskForm):
    nombre = StringField("Nombre", validators=[InputRequired(), Length(min=2, max=120)])
    contacto = StringField(
        "Contacto (email o teléfono)", validators=[InputRequired(), Length(min=5, max=200)]
    )
    tipo = SelectField("Tipo", choices=TIPOS, validators=[InputRequired()])
    mensaje = TextAreaField("Mensaje", validators=[InputRequired(), Length(min=10, max=2000)])
    website = StringField("No completar")  # honeypot
