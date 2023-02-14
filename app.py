from flask import Flask, request, render_template, redirect, url_for
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imwrite(image_path, img)
    return redirect(url_for('uploaded_image', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_image(filename):
    return render_template('index.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
