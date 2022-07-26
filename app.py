from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nacehrgeaegyja:8c518e59d0b2c65644904063311acaebba98d7376d9064b77e5f2520c97a3a47@ec2-44-206-197-71.compute-1.amazonaws.com:5432/dfdi2279vjc4ke'

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
