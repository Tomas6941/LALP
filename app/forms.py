from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired, Length

from content import mle


class ContactForm(FlaskForm):
    nombre = StringField("Nombre", validators=[InputRequired(), Length(min=2, max=120)])
    contacto = StringField(
        "Contacto (email o teléfono)", validators=[InputRequired(), Length(min=5, max=200)]
    )
    puesto = SelectField(
        "Equipo al que querés sumarte",
        choices=mle.PUESTOS,
        validators=[InputRequired()],
    )
    mensaje = TextAreaField(
        "¿Por qué te sumás? (experiencia, ideas, disponibilidad)",
        validators=[InputRequired(), Length(min=10, max=2000)],
    )
    website = StringField("No completar")  # honeypot


class LoginForm(FlaskForm):
    usuario = StringField("Usuario", validators=[InputRequired(), Length(min=1, max=120)])
    password = StringField("Contraseña", validators=[InputRequired(), Length(min=1, max=200)])