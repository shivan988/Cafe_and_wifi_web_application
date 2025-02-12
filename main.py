from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, URLField, SubmitField
from wtforms.validators import DataRequired


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
app.config['SECRET_KEY'] = "this_is_very_secret"
db.init_app(app)
Bootstrap5(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    cafe_name: Mapped[str] = mapped_column(unique=True)
    coffee: Mapped[str] = mapped_column()
    wifi: Mapped[str] = mapped_column()
    socket: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column()


with app.app_context():
    db.create_all()


class CafeForm(FlaskForm):
    cafe_name = StringField(label="Cafe_name", validators=[DataRequired()])
    coffee = SelectField(label='Coffee rating', choices=[" ", "☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                         validators=[DataRequired()])
    wifi = SelectField(label='Wifi rating', choices=[' ', '🛜', '🛜🛜', '🛜🛜🛜', '🛜🛜🛜🛜', '🛜🛜🛜🛜🛜'],
                       validators=[DataRequired()])
    socket = SelectField(label='Socket available', choices=[' ', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
                         validators=[DataRequired()])
    location = URLField(label='Location', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list_of_cafes')
def list_of_cafes():
    cafes_list = db.session.execute(db.select(Cafe)).scalars()
    return render_template("list_of_cafes.html", cafes=cafes_list)


@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe_name.data
        coffee = form.coffee.data
        wifi = form.wifi.data
        socket = form.socket.data
        location = form.location.data

        new_cafe = Cafe(
            cafe_name=cafe_name,
            coffee=coffee,
            wifi=wifi,
            socket=socket,
            location=location,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('list_of_cafes'))
    return render_template('add_cafe.html', form=form)


@app.route('/delete/<int:id>')
def delete(id):
    cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id==id)).scalar()
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('list_of_cafes'))


if __name__ == "__main__":
    app.run(debug=True)
