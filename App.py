#############################################################################################################

from flask import Flask, render_template, request, redirect, url_for, flash
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Load the pre-trained model
model = load_model('model.h5')

# Define the classes (replace with your actual class names)
CLASS_NAMES = ['Bear', 'Bird', 'Cat', 'Cow', 'Deer', 'Dog', 'Dolphin', 'Elephant', 'Giraffe', 'Horse', 'Kangaroo', 'Lion', 'Panda', 'Tiger', 'Zebra']  

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory "database" to store image paths and predictions
image_db = []

# Function to preprocess the image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  #  input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image
    return img_array

# Function to predict the class
def predict_image(img_path):
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence = np.max(predictions) * 100
    return predicted_class, confidence

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded!', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(request.url)

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Predict the class
        predicted_class, confidence = predict_image(file_path)

        # Add the image and prediction to the "database"
        image_db.append({
            'image_url': file_path,
            'predicted_class': predicted_class,
            'confidence': confidence
        })

        # Render the result on the same page
        return render_template('index.html', image=image_db[-1], show_result=True)

    return render_template('index.html', show_result=False)

@app.route('/history')
def history():
    # Pass the enumerate function to the template context
    return render_template('history.html', images=image_db, enumerate=enumerate)

@app.route('/delete/<int:index>')
def delete_image(index):
    # Delete a specific image from the history
    if 0 <= index < len(image_db):
        deleted_image = image_db.pop(index)
        os.remove(deleted_image['image_url'])  # Delete the file from the server
        flash('Image deleted successfully!', 'success')
    else:
        flash('Invalid image index!', 'error')
    return redirect(url_for('history'))

@app.route('/delete_all')
def delete_all():
    # Delete all images from the history
    for image_data in image_db:
        os.remove(image_data['image_url'])  # Delete all files from the server
    image_db.clear()
    flash('All images deleted successfully!', 'success')
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)