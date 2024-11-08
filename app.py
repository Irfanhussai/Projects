import os
import random
from flask import Flask, redirect, render_template, request, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model for storing credentials
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
   

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Create the database and tables if they don't exist
with app.app_context():
    db.create_all()

# Load disease information
try:
    disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
    supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')
except Exception as e:
    print(f"Error loading CSV files: {e}")

# Load model
try:
    model = CNN.CNN(39)
    model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Prediction function
def prediction(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((224, 224))
        input_data = TF.to_tensor(image)
        input_data = input_data.view((-1, 3, 224, 224))
        output = model(input_data)
        output = output.detach().numpy()
        index = np.argmax(output)
        return index
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

# Generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Routes
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        otp = generate_otp()
        session['otp'] = otp
        # Implement email sending logic here, e.g., using Flask-Mail or other email API
        print(f"OTP for {email}: {otp}")  # Replace with actual email sending in production

        flash('Registration successful! Check your email for OTP verification.')
        return redirect(url_for('verify_otp'))
    
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash ('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash ('Invalid username or password. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login_page'))

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = secure_filename(image.filename)
        file_path = os.path.join('static/uploads', filename)
        image.save(file_path)
        
        pred = prediction(file_path)
        if pred is not None:
            title = disease_info['disease_name'][pred]
            description = disease_info['description'][pred]
            prevent = disease_info['Possible Steps'][pred]
            image_url = disease_info['image_url'][pred]
            supplement_name = supplement_info['supplement name'][pred]
            supplement_image_url = supplement_info['supplement image'][pred]
            supplement_buy_link = supplement_info['buy link'][pred]
            return render_template('submit.html', title=title, desc=description, prevent=prevent,
                                   image_url=image_url, pred=pred, sname=supplement_name,
                                   simage=supplement_image_url, buy_link=supplement_buy_link)
        else:
            flash('Prediction failed. Please try again.')
            return redirect(url_for('home_page'))

@app.route('/market')
def market():
    return render_template('market.html', supplement_image=list(supplement_info['supplement image']),
                           supplement_name=list(supplement_info['supplement name']),
                           disease=list(disease_info['disease_name']),
                           buy=list(supplement_info['buy link']))

@app.route('/dashboard')
def dashboard():
    sensor_data = {
        'soil_moisture': 70,
        'temperature': 25
    }
    pump_status = session.get('pump_status', False)
    return render_template('dashboard.html', sensor_data=sensor_data, pump_status=pump_status)

@app.route('/dashboard/index')
def dashboard_index():
    # Any necessary logic before rendering the page
    return render_template('index.html') 

@app.route('/toggle_pump', methods=['POST'])
def toggle_pump():
    pump_status = not session.get('pump_status', False)
    session['pump_status'] = pump_status
    return jsonify({'status': 'success', 'pump_status': pump_status})

if __name__ == '__main__':
    app.run(debug=True)
