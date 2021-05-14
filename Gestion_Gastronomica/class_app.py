#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO



from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Length
from flask_login import UserMixin, current_user


from werkzeug.security import generate_password_hash, check_password_hash


class SignForm(FlaskForm):
    num_adultos = IntegerField('num_adultos', validators=[DataRequired("Must be an integer between 0 and 10"), NumberRange(0,10, "Must be an integer between 0 and 10") ])
    num_niños = IntegerField('num_niños', validators=[DataRequired("Must be an integer between 0 and 10"),  NumberRange(0,10, "Must be an integer between 0 and 10") ])
    cod_mesa = StringField('cod_mesa', validators=[DataRequired(), Length(max=10)])
    nick = StringField('Nick', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Empezar')

class ReSignForm(FlaskForm):
    nick = StringField('Nick', validators = [DataRequired(), Length(max=10)])
    cod_mesa = StringField('code_mesa', validators = [DataRequired(), Length(max=10)])
    submit = SubmitField('Ordenar')

class LoginForm(FlaskForm):
    cod_mesa = StringField("cod_mesa", validators = [DataRequired(), Length(max=10)])
    nick = StringField("nick", validators = [DataRequired(), Length(max=10)] )
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Entrar")

class Loging(UserMixin):
    def __init__ (self, id, num_adultos, num_niños, cod_mesa, nick):
        self.id = id
        self.num_adultos = num_adultos
        self.num_niños = num_niños
        self.cod_mesa = cod_mesa
        self.nick = nick
    def __repr__(self):
        return '<Login {}>'.format(self.id)


class Upload_mesa(FlaskForm):
    id = IntegerField('id', validators=[DataRequired("Must be an integer between 0 and 10"), NumberRange(0,10, "Must be an integer between 0 and 10") ])
    Ubicacion = StringField('ubicacion', validators=[DataRequired(),  Length(max=10) ])
    Tipo_Silla = StringField('tipo_silla', validators=[DataRequired(), Length(max=10)])
    Comensales_Maximo = IntegerField('comensales_maximo', validators=[DataRequired("Must be an integer between 0 and 10"), NumberRange(0,10, "Must be an integer between 0 and 10") ])
    submit = SubmitField('Empezar')

if __name__ == "__init__":
    print("Todo mal si me lees")