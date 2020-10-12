from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/board'
app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ActivityModel(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer())
    activity = db.Column(db.String(120), unique=True)

    def __init__(self, hours, activity):
        self.hours = hours
        self.activity = activity

    def __repr__(self):
        return f"<Car {self.activity}>"

@app.route('/')
def hello_world():
    return "myUser"

@app.route('/activities', methods=['GET', 'POST'])
def handle_activities():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_activity = ActivityModel(activity=data['activity'], hours=data['hours'])
            db.session.add(new_activity)
            db.session.commit()
            return {"message": f"Activity {new_activity.activity} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        activities = ActivityModel.query.all()
        results = [{
            "id": activity.id,
            "hours": activity.hours,
            "activity": activity.activity,
        } for activity in activities]

        return {"count": len(results), "activities": results}

if __name__ == "__main__":
    app.run()
