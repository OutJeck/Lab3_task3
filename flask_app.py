import MAIN
from flask import Flask, request, render_template, url_for, redirect


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global name
        name = request.form['contents']
        MAIN.creating_app(name)
        return redirect(url_for('map'))
    if request.method == "GET":
        return render_template("mysite.html")


@app.route("/map", methods=["GET"])
def map():
    return render_template(f"{name}_map.html")
