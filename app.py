from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np


# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.utils import load_img, img_to_array

# importing tensorflow for prediction
import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# Flask utils
from flask import Flask, redirect, url_for, request, render_template, session, jsonify

# Define a flask app
app = Flask(__name__)
app.secret_key = 'mysecretkey'

from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
import json

# convert the ObjectId to a string
obj_id = ObjectId('615ef2a1f73dd31c609de91f')
str_id = str(obj_id)


# Define database connection
client = MongoClient('mongodb+srv://sopolaw345:123@srm.uhy7bqk.mongodb.net')
db = client['Plantix']
users = db['users']
contacts = db['contacts']

# Model saved with Keras model.save()
MODEL_PATH = 'models/hackmodel.h5'

# Load your trained model
model = load_model(MODEL_PATH)


class_descriptions = {
    'Grassy Shoots': 'Your plant is affected by grassy shoots disease. This disease is characterized by the presence of grassy-like shoots emerging from the stem of the plant. The cause of this disease is a viral infection, and there are no known remedies for it. It is recommended to remove the affected plant as soon as possible to prevent the spread of the disease to other plants.',
    'Healthy': 'Congratulations! Your plant is healthy and there are no signs of disease or infection. Keep up the good work by regularly watering and fertilizing your plant.',
    'Mites': 'Your plant is affected by mites. This disease is characterized by small, spider-like insects on the plant. The mites feed on the plant sap, causing yellowing of the leaves and stunted growth. To treat this disease, you can use a solution of neem oil or insecticidal soap. Regularly pruning the affected parts of the plant can also help control the spread of the disease.',
    'Ring Spot': 'Your plant is affected by ring spot disease. This disease is characterized by the appearance of circular or ring-like spots on the leaves. The cause of this disease is a fungal infection, and there are no known remedies for it. To prevent the spread of the disease, it is recommended to remove the affected leaves and ensure that the plant is well-ventilated.',
    'YLD': 'Your plant is affected by yellow leaf disease. This disease is characterized by the yellowing of the leaves and stunted growth. The cause of this disease is a nutrient deficiency, and it can be treated by adding a fertilizer rich in nitrogen, phosphorus, and potassium. Regularly watering the plant can also help promote growth.'
}

def model_predict(img_path, model):
    class_names=['Grassy Shoots', 'Healthy', 'Mites', 'Ring Spot', 'YLD']
    

    img = Image.open(img_path)

    img=img.resize((256,256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)

    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence




@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        contact = {'name': name, 'email': email, 'message': message}
        contacts.insert_one(contact)

        # Set success message and redirect to signup page
        success_message = 'Form Submited successfully'
        return render_template('contact.html', success_message=success_message)
        
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect')
def detect():
    if 'user' not in session:
        return redirect('/login')
    else:
        # Get user ID from session and fetch user data from the database
        user_id = ObjectId(session['user'])
        user = users.find_one({'_id': user_id})
        return render_template('detect.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        user = users.find_one({'email': email})
        if user:
            # User exists, check password
            if user['password'] == password:
                # Passwords match, store user data in session and redirect to dashboard
                # store the string in the session as JSON
                user_id_str = str(user['_id'])  # store user ID in session
                session['user'] = user_id_str

                # Return the user's ID as a JSON response
                response_data = {'_id': user_id_str}

                # Allow access to the response from any origin (replace '*' with a specific origin if needed)
                response = jsonify(response_data)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
                success_message = 'Login successfull!'
                return redirect('/detect')
                return jsonify({'success': success})
            else:
                # Passwords don't match, show error message
                error_message = 'Password does not match'
                return jsonify({'error': error_message})
        else:
            # User doesn't exist, show error message
            error_message = 'User not found'
            return jsonify({'error': error_message})

    # Render login page
    return render_template('login.html')


# Define signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if email is already registered
        if users.find_one({'email': email}):
            # Email is already registered
            error_message = 'Email is already registered'
            return render_template('signup.html', error_message=error_message)
        else:
            # Email is not registered, create new user
            user = {'name': name, 'email': email, 'password': password}
            users.insert_one(user)

            # Set success message and redirect to signup page
            success_message = 'User created successfully'
            return render_template('signup.html', success_message=success_message)

    # Render signup page
    return render_template('signup.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            # Get the file from post request
            f = request.files['file']

            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                basepath, 'uploads', secure_filename(f.filename))
            f.save(file_path)

            # Make prediction
            predicted_class, confidence = model_predict(file_path, model)
            
            
            # Get the class description based on the predicted class
            class_description = class_descriptions[predicted_class]
        
            return predicted_class
            
        except Exception as e:
            # If an error occurs, capture the error message and return it as an alert message in JavaScript.
            error_message = str(e)
            return f"Please Provide Valid Image!"
    return None
    
    
    
if __name__ == '__main__':
    app.run(debug=True)


