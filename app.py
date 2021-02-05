"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "cup"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return a list of cupcakes as JSON"""
    cup = Cupcake.query.all()
    cupcakes = [cc.serialized() for cc in cup]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>")
def list_cupcake(id):
    """Return cupcake information on id as JSON"""
    cup = Cupcake.query.get_or_404(id)
    cupcake = cup.serialized()
    return jsonify(cupcake=cupcake)

@app.route("/api/cupcakes", methods=["POST"])
def make_cupcake():
    """Add a cupcake and return cupcake information as JSON"""
    cupcake = Cupcake(
        flavor = request.json["flavor"],
        rating = request.json["rating"],
        size = request.json["size"],
        image = request.json["image"] or None)
    
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialized()), 201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Updates cupcake information"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake and return a message for confirmation"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return json(message="Cupcake was Deleted!")