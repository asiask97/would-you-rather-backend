from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") 

# Initialize the database 
db = SQLAlchemy(app)
ma = Marshmallow(app)
# Create Model
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    optionOne = db.Column(db.String(700), nullable=False)
    optionTwo = db.Column(db.String(700), nullable=False)

class Answers(db.Model):
    q_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key = True)    
    optionOne = db.Column(db.Integer)
    optionTwo = db.Column(db.Integer)


class QuestionsShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Questions

class AnswersShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answers

@app.route('/', methods = ['GET', 'POST'])
def index():
   
    if request.method == 'GET':
        data = Questions.query.all()
        q_schema = QuestionsShema()
        output = q_schema.dump(data, many=True)
        return jsonify({'qustions': output})
    
    if request.method == 'POST':
        data = request.json
        add = Answers.query.filter_by(q_id =data['question']).first()
        if data['option'] == 'one':
            if add.optionOne == 0:
                add.optionOne = 1
            else:
                add.optionOne += 1

        if data['option'] == 'two':
            if add.optionTwo == 0:
                add.optionTwo = 1
            else:
                add.optionTwo += 1


        db.session.commit()
       
        a_schema = AnswersShema()
        output = a_schema.dump(add)
        return jsonify({'awnsers': output})
    


@app.route('/results', methods = ['GET'])
def anwsers():
   
    if request.method == 'GET':
        data = Answers.query.all()
        a_schema = AnswersShema()
        output = a_schema.dump(data, many=True)
        return jsonify({'anwsers': output})
    


if __name__ == "__main__":
    app.run(debug=True)
