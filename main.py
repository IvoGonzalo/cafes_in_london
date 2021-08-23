from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Length
import os


app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = os.environ.get('CAFE_API_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired(), Length(max=35)])
    map_url = StringField("Cafe Location on Google Mapas (URL)", validators=[DataRequired(), URL(message="Please write a correct url")])
    img_url = StringField("Image URL", validators=[DataRequired(), URL(message="Please write a correct url")])
    location = StringField("Cafe Location", validators=[DataRequired(), Length(max=20)])
    seats = SelectField("How many seats?", choices=["10-20", "20-30", "30-40", "+50"], validators=[DataRequired()])
    has_toilet = SelectField("Has Toilet?", choices=["Yes", "No"], validators=[DataRequired()])
    has_wifi = SelectField("Has Wifi?", choices=["Yes", "No"], validators=[DataRequired()])
    has_sockets = SelectField("Has Sockets?", choices=["Yes", "No"], validators=[DataRequired()])
    can_take_calls = SelectField("Can take calls?", choices=["Yes", "No"], validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired(), Length(max=5)])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    return render_template("index.html", cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def post_new_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if form.has_toilet.data == "Yes":
            has_toilet = 1
        else:
            has_toilet = 0
        if form.has_wifi.data == "Yes":
            has_wifi = 1
        else:
            has_wifi = 0
        if form.has_sockets.data == "Yes":
            has_sockets = 1
        else:
            has_sockets = 0
        if form.can_take_calls.data == "Yes":
            can_take_calls = 1
        else:
            can_take_calls = 0

        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
    return render_template("add.html", form=form)


@app.route("/delete")
def delete():
    cafe_id = request.args.get('id')
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect('/#background')


if __name__ == '__main__':
    app.run(debug=True)