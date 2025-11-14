from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

class FormularioLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class FormularioRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(), 
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), 
        EqualTo('contraseña', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Registrarse')

class FormularioProducto(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=500)])
    precio = FloatField('Precio', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int)
    imagen = FileField('Imagen del Producto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes permitidas')
    ])
    submit = SubmitField('Guardar Producto')