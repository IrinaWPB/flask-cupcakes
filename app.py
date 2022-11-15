from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.config["CORS_SUPPORTS_CREDENTIALS"]=True
connect_db(app)


@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""

    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

# *****************************
# RESTFUL CUPCAKES JSON API
# *****************************

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all todos"""

    all_cupcakes = [cc.serialize() for cc in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake in particular"""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""

    new_cupcake = Cupcake(flavor=request.json["flavor"],
                        size=request.json["size"],
                        rating=request.json["rating"],
                        image=request.json.get("image", "https://tinyurl.com/demo-cupcake"))
    db.session.add(new_cupcake)
    db.session.commit()
    
    return (jsonify(cupcake=new_cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""

    cc = Cupcake.query.get_or_404(id)
    cc.flavor = request.json.get('flavor', cc.flavor),
    cc.size = request.json.get('size', cc.size),
    cc.rating = request.json.get('rating', cc.rating),
    cc.image = request.json.get('image', cc.image),
    db.session.commit()
    return jsonify(cupcake=cc.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")

