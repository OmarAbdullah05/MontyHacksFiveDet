import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)



@app.route('/')
def home():
    return render_template('index.html')

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/video')
def video():
    return render_template('stream.html')
@app.route('/vid')
def vid():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)