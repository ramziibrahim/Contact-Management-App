from flask import request, jsonify #jsonify allows us to return json data
from config import app, db
from models import Contact

#display contents
@app.route("/contacts", methods=["GET"]) # decorator that goes above a function (specifcy what route we want, then say the method (GET, DELETE, ETC.))
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts)) # map takes all the elements from contacts list and makes a new list with json data
    return jsonify({"contacts": json_contacts})

#add new contact
@app.route("/create_contact", methods=["POST"])
def create_contact():   
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email"}),
            400,    #let the user know that it was unsuccessful by returning a 400 error message
        )

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)          # then add to db session
        db.session.commit()                  # then commit it so now anything in session actually is written into database 
    except Exception as e:                   # catch any exceptions then return a status 400 (fail)
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201   # 201 means user is created, u could also just use 200

#update contact
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):                # whatevers being passed should match the thing where ("user_id") is
    contact = Contact.query.get(user_id)    # looks through database and finds user with specific id

    if not contact:
        return jsonify({"message": "User not found"}), 404  #Status code 404 because we did not find contact

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)   #makes the new first name from user equal to first name we stored before that we are requesting data from
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "Usr updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)