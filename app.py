from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

current_time = datetime.now()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Amulya%4010@127.0.0.1:3306/patient_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

chat_history = []

db = SQLAlchemy(app)

# Database models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(15), nullable=False)  # Make sure this line exists
    email = db.Column(db.String(50), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        email = request.form['email']
        
        new_patient = Patient(name=name, age=age, gender=gender, contact=contact, email=email)
        db.session.add(new_patient)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_patient.html')

@app.route('/view_patients')
def view_patients():
    patients = Patient.query.all()
    return render_template('view_patients.html', patients=patients)

# Chatbot Route
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.form.get('user_input')  # Safely get form input
        if user_input:
            # Here you can call your chatbot response generation logic
            chatbot_response = generate_chatbot_response(user_input)
            # Save user input and response to chat history
            chat_history.append({'timestamp': datetime.now(), 'user': user_input, 'bot': chatbot_response})
        return redirect(url_for('chatbot'))  # Redirect to refresh the chat page

    # For GET request, render the chat history
    return render_template('chatbot.html', chat_history=chat_history)

def generate_chatbot_response(user_input):
    # Dummy function - replace with actual chatbot logic
    return f"You said: {user_input}"

if __name__ == '__main__':
    with app.app_context():

        db.create_all()
    app.run(debug=True)
