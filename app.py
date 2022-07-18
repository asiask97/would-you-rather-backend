from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qanda.db'
# Initialize the database 
db = SQLAlchemy(app)
ma = Marshmallow(app)
# Create Model
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(700), nullable=False)
    optionOne = db.Column(db.String(700), nullable=False)
    optionTwo = db.Column(db.String(700), nullable=False)
    def __repr__(self):
        return '<Questions %r%r%r>' % (self.question, self.optionOne, self.optionTwo)
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
        return jsonify({'questions': output})
    
    if request.method == 'POST':




if __name__ == "__main__":
    app.run(debug = True)
    db.create_all()
    db.session.add_all(users)
    db.session.commit()
    app.run()