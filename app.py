from flask import Flask
from flask import render_template
from flask import request,redirect,flash
from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///D:\\movieapp\\moviedatabase.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Movie(db.Model):
	__tablename__ = "movie"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	location = db.Column(db.String, nullable=False)
	time = db.Column(db.String, nullable=False)

@app.route('/', methods=["GET", "POST"])
def home():
    movies = None
    if request.form:
        try:
            movie = Movie(title=request.form.get("title"), location=request.form.get("location"), time=request.form.get("time"))
            db.session.add(movie)
            db.session.commit()
        except Exception as e:
            print("Failed to add movie")
            print(e)
    movies = Movie.query.all()
    return render_template("dashboard.html", movies=movies)

@app.route("/delete", methods=["GET","POST"])
def delete():
    title = request.form.get("title")
    movie = Movie.query.filter_by(title=title).first()
    if movie is None:
    	return redirect("/")
    db.session.delete(movie)
    db.session.commit()
    return redirect("/")

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    newlocation = request.form.get("newlocation")
    newtime = request.form.get("newtime")
    kid = request.form.get("id")
    movie = Movie.query.filter_by(title=oldtitle).first()
    if movie is None:
    	return redirect("/")
    movie.title = newtitle
    movie.location = newlocation
    movie.time = newtime
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
	manager.run()
