from flask import Flask, request,jsonify, abort
from flask_sqlalchemy import SQLAlchemy
# postgresql://postgres:123456@localhost/python
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/python'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'
db = SQLAlchemy(app)
class fromdata(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fname= db.Column(db.String(50))
    lname= db.Column(db.String(50))
    address= db.Column(db.String(120))
    city= db.Column(db.String(15))
    conn= db.Column(db.Integer())
    
    def __init__(self, fname, lname, address, city, conn):
        
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.conn = conn
        
@app.route("/")
def home():
    return {"msg":"ok"}


@app.route('/pets', methods = ['POST'])
def create_pet():
    pet_data = request.json

    fname = pet_data['fname']
    lname = pet_data['lname']
    address = pet_data['address']
    city = pet_data['city']
    conn = pet_data['conn']
    pet = fromdata(fname =fname , lname = lname, address = address, city =city , conn=conn)
    db.session.add(pet)
    db.session.commit()
    

    return jsonify({"success": True,"response":"Pet added"}) 
        
@app.route('/getpets', methods = ['GET'])
def getpets():
     all_pets = []
     pets = fromdata.query.all()
     for pet in pets:
          results = {
                    "id":pet.id,
                    "fname":pet.fname,
                    "lname":pet.lname,
                    "address":pet.address,
                    "city":pet.city,
                    "conn":pet.conn,}
          all_pets.append(results)

     return jsonify(
            {
                "success": True,
                "pets": all_pets,
                "total_pets": len(pets),
            }
        )

@app.route("/pets/<int:id>", methods = ["PUT"])
def update_pet(id):
    id = fromdata.query.get(id)
    fname = request.json['fname']
    lname = request.json['lname']
    address = request.json['address']
    city = request.json['city']
    conn = request.json['conn']
    
    if id is None:
        abort(404)
    else:
        id.fname = fname
        id.lname = lname
        id.address = address
        id.city = city
        id.conn = conn
        db.session.add(id)
        db.session.commit()
        return jsonify({"success": True, "response": "Pet Details updated"})


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_pet(id):
        response = {}
        id = fromdata.query.get(id)
        response['id'] = id
        db.session.delete(id)
        db.session.commit()
        return  jsonify({"success": True, "response": "Pet Details Delete"})


if __name__ == '__main__':
        app.run(debug=True)
        db.create_all()
        app.run()