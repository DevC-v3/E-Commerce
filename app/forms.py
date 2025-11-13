from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo

class FormularioLogin(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])

class FormularioRegistro(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(2, 100)])
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired(), Length(6, 100)])
    confirmar_contrasena = PasswordField('Confirmar Contraseña', 
                                       validators=[DataRequired(), EqualTo('contrasena')])
    direccion = TextAreaField('Dirección')
    telefono = StringField('Teléfono')

class FormularioCheckout(FlaskForm):
    direccion_envio = TextAreaField('Dirección de Envío', validators=[DataRequired()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    codigo_postal = StringField('Código Postal', validators=[DataRequired()])
    metodo_pago = SelectField('Método de Pago', 
                            choices=[('tarjeta', 'Tarjeta de Crédito/Débito'), 
                                   ('paypal', 'PayPal')],
                            validators=[DataRequired()])

class FormularioReseña(FlaskForm):
    calificacion = SelectField('Calificación', 
                             choices=[(1, '1 Estrella'), (2, '2 Estrellas'), 
                                    (3, '3 Estrellas'), (4, '4 Estrellas'), 
                                    (5, '5 Estrellas')],
                             coerce=int,
                             validators=[DataRequired()])
    comentario = TextAreaField('Comentario', validators=[Length(0, 500)])