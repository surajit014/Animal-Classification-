Project Structure :-

Users can upload an image, and the app predicts the animal and displays the result on the same page.

There is a History option (a separate page) where users can view all uploaded images and their predictions.

Users can delete history data:

Delete one image at a time.

Delete all images at once.

animal_classification_app/ ├── static/

│ ├── uploads/ # Folder to store uploaded images

│ └── styles.css # Optional: For custom CSS

├── templates/

│ ├── index.html # Home page for uploading and prediction

│ └── history.html # History page to view and delete images

├── app.py # Flask application

├── model.h5 # Your MobileNetV2 model

└── requirements.txt # Python dependencies

Features Upload and Predict: Users can upload an image and see the prediction.

History: Users can view all uploaded images and their predictions.

Delete: Users can delete one image at a time or delete all images at once.
