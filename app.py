from flask import Flask, render_template, request, redirect
from transformers import pipeline
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/db'
db = SQLAlchemy(app)

classifier = pipeline('sentiment-analysis')

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(255))
    ai_response = db.Column(db.String(255))

@app.route('/', methods=['GET', 'POST'])
def index():
    ai_response = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        ai_response = get_sentiment(user_input)
        interaction = Interaction(user_input=user_input, ai_response=ai_response)
        db.session.add(interaction)
        db.session.commit()
    return render_template('index.html', ai_response=ai_response)

def get_sentiment(text):
    result = classifier(text)
    return result[0]['label']

if __name__ == '__main__':
    # Create all database tables before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)
