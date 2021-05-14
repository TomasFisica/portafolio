#autor : Tomas E. García Fernández
#email : tomas.garcia.fisica@gmail.com
#	    tomas.garcia.fisica@hotmail.com
#Linkedin: www.linkedin.com/in/tomas-garcia-fisica
# Desarrollo en PROCESO


#Lib to import

#Flask, MySQL, SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy
#Propias
from functions import Acceso, get_user
from class_app import SignForm, ReSignForm, LoginForm,Loging, Upload_mesa

app = Flask(__name__)
app.config['SECRET_KEY'] = '6767676'
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'mysql://leo@localhost:octavio_1004/gastroecosistem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "Sign"

db = SQLAlchemy(app)

class Mesa(db.Model):
    __tablename__ = "mesas"

    idMesa = db.Column(db.Integer, primary_key = True)
    Ubicacion = db.Column(db.Enum('Ventana','Barra','Baño','Balcon','Ambiente único','Vereda','Patio Techo','Patio libre','Terraza','Pasillo angosto'))
    ComensalesMaximo = db.Column(db.Integer)
    Tipo_Silla = db.Column(db.Enum('Silla común','Sillon','Banquetas'))

    def __repr__(self):
        return f'<User {self.email}>'
    def save(self):
        if not self.idMesa:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idMesa):
        return Mesa.query.get(idMesa)


#Route
@app.route("/", methods = ["GET", "POST"])
def Sign():
    print("dic_mesas", dic_mesas, "dic_ses", dic_ses)
    if current_user.is_authenticated:
        return redirect(url_for("Menu"))
    form = SignForm()
    if form.validate_on_submit():
        num_adultos = form.num_adultos.data
        num_niños =  form.num_niños.data
        cod_mesa =  form.cod_mesa.data
        nick = form.nick.data
        status = Acceso(int(dic_ses["id"][-1])+1,num_adultos, num_niños, cod_mesa, nick, dic_ses, dic_mesas)
        next = request.args.get('next', None)
        if status:
            form_to_sign = Loging(dic_ses["id"][-1],num_adultos, num_niños, cod_mesa, nick)
            users.append(form_to_sign)
            login_user(form_to_sign, remember = True)
            if current_user.is_authenticated:
                return redirect(url_for("Menu"))
        else:
            return redirect(url_for("Sign"))
      
    return render_template("sign.html", name_rest = "Mi restaurante", form = form)


@login_manager.user_loader
def Load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route("/menu", methods = ["GET", "POST"])
@login_required
def Menu():
    form_mesa = Upload_mesa()
    if form_mesa.validate_on_submit():
        idMesa = form_mesa.id.data
        ubicacion = form_mesa.Ubicacion.data
        tipo_silla = form_mesa.Tipo_Silla.data
        comensales_maximo = form_mesa.Comensales_Maximo.data
        mesa_nueva = Mesa(idMesa = idMesa, Ubicacion = ubicacion, ComensalesMaximo = comensales_maximo, Tipo_Silla = tipo_silla)
        mesa_nueva.save()
    return render_template("menu.html", name_rest = "Mi restaurante", form = form_mesa)

@app.route("/resign", methods = ["GET", "POST"])
def ReSign():
    if current_user.is_authenticated:
        return redirect(url_for("Menu"))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.nick.data, form.cod_mesa.data, users)
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        print("next", next_page)
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("Menu")
        return redirect(next_page)    
    return render_template("resign.html", name_rest = "Mi restaurante", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect (url_for('Sign'))



######################################################
#   Variables MOMENTANEAS hasta que se implemente la base de datos
######################################################
id = [0]
dic_mesas = {"001" : False, "002" : False, "003":False, "004": False}
dic_ses = {"id" : [0], "num_adultos" :[None], "num_niños": [None], "cod_mesa" : [None], "nick":[None] }
users = []
if __name__ == "__main__":
    
    app.run(debug = True)