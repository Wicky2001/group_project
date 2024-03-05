from flask import Flask, render_template
import threading

app = Flask(__name__)


def run_model():
    from model import pipeline
    # Initialize and run the model
    model = pipeline.detector()
    result = model.detect()


@app.route('/')
def home():
    return render_template(r'html/home.html')


@app.route('/detect', methods=['GET'])
def detect():
    model_thread = threading.Thread(target=run_model)
    model_thread.start()


    # Process the result and return a response if needed
    return render_template(r'html/detect.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    print("Server is running...")
