from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- MODELS --------------------
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    diagnosis = db.Column(db.String(200))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    doctor = db.Column(db.String(100))

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))

# -------------------- ROUTES --------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/patients')
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    diagnosis = request.form['diagnosis']
    new_patient = Patient(name=name, age=age, gender=gender, diagnosis=diagnosis)
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('patients'))

@app.route('/appointments')
def appointments():
    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_id = request.form['patient_id']
    date = request.form['date']
    time = request.form['time']
    doctor = request.form['doctor']
    new_appointment = Appointment(patient_id=patient_id, date=date, time=time, doctor=doctor)
    db.session.add(new_appointment)
    db.session.commit()
    return redirect(url_for('appointments'))

@app.route('/bills')
def bills():
    all_bills = Bill.query.all()
    return render_template('bills.html', bills=all_bills)

@app.route('/add_bill', methods=['POST'])
def add_bill():
    patient_id = request.form['patient_id']
    amount = request.form['amount']
    status = request.form['status']
    new_bill = Bill(patient_id=patient_id, amount=amount, status=status)
    db.session.add(new_bill)
    db.session.commit()
    return redirect(url_for('bills'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
