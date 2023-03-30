from flask import Flask, render_template, jsonify
import json

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='template')

app.config["DEBUG"] = True

@app.route('/data')
def get_data():
    with open('sample.json', 'r') as f:
        data = json.load(f)
    return data


@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host = 'localhost', port=8000, debug = True)