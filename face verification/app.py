from flask import Flask, render_template, request, jsonify
import face_recognition
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    file1 = request.files['image1']
    file2 = request.files['image2']

    path1 = os.path.join(UPLOAD_FOLDER, 'img1.jpg')
    path2 = os.path.join(UPLOAD_FOLDER, 'img2.jpg')

    file1.save(path1)
    file2.save(path2)

    img1 = face_recognition.load_image_file(path1)
    img2 = face_recognition.load_image_file(path2)

    enc1 = face_recognition.face_encodings(img1)
    enc2 = face_recognition.face_encodings(img2)

    if len(enc1) == 0 or len(enc2) == 0:
        return jsonify({'result': '❌ No face detected!'})

    match = face_recognition.compare_faces([enc1[0]], enc2[0])[0]

    if match:
        return jsonify({'result': '✅ Face Matched!'})
    else:
        return jsonify({'result': '❌ Face Not Matched!'})

if __name__ == '__main__':
    app.run(debug=True)