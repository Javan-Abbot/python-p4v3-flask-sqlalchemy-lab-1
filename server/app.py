# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    
    if earthquake is None:
        body = {"message": f"Earthquake {id} not found."}
        return make_response(body, 404)
    body = {
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    }
    return make_response(body, 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def test_earthquake(magnitude):
    earthquake = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    earthquake_list = []
    for quake in earthquake:
        earthquake_data = {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        earthquake_list.append(earthquake_data)
        
    response_body = {
            "count": len(earthquake_list),
            "quakes": earthquake_list
        }
        
    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
