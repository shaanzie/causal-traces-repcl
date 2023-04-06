from flask import Flask, render_template, jsonify
import pandas as pd
import json
import numpy as np

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='template')

app.config["DEBUG"] = True

@app.route('/data')
def get_data():
    generate_trace(r'./LOG/tiny_sample.log')
    with open('generated_trace.json', 'r') as f:
        data = json.load(f)
    return data

def find_send_clock(row):

    offsets = row['e.offsets'].split('-')
    counters = row['e.counters'].split('-')
    epoch = row['e.max_epoch']
    clock = []
    for i in range(len(offsets)):
        clock.append(epoch + int(offsets[i]) + int(counters[i]))

    return clock

def find_recv_clock(row):

    offsets = row['f.offsets'].split('-')
    counters = row['f.counters'].split('-')
    epoch = row['f.max_epoch']
    clock = []
    for i in range(len(offsets)):
        clock.append(epoch + int(offsets[i]) + int(counters[i]))

    return clock

def generate_trace(csv_file: str):
    columns = [
        'e',
        'f',
        'e.max_epoch',
        'e.offsets',
        'e.offset_size',
        'e.counters',
        'e.counter_size',
        'f_old.max_epoch',
        'f_old.offsets',
        'f_old.offset_size',
        'f_old.counters',
        'f_old.counter_size',
        'f.max_epoch',
        'f.offsets',
        'f.offset_size',
        'f.counters',
        'f.counter_size',
        'f.max_counter',
        'epsilon',
        'perceived_epsilon',
        'interval',
        'alpha',
        'delta'
    ]
    df = pd.read_csv(csv_file, names = columns)
    print('File read successful!')
    df['failure'] = 0
    df.loc[np.random.rand(len(df)) < 0.1, 'failure'] = 1
    df['msg'] = 'Dummy message'
    df['e.clock'] = df.apply(lambda row: find_send_clock(row), axis = 1)
    df['f.clock'] = df.apply(lambda row: find_recv_clock(row), axis = 1)
    print('Found clocks!')
    df_sorted = df.sort_values(by='e.clock', key=lambda x: x.apply(lambda y: sum(y)))
    print('Ordered events!')
    df_sorted = df[['e', 'f', 'e.clock', 'f.clock', 'failure', 'msg']]
    df_sorted.to_json('generated_trace.json', orient = 'records')
    print('JSON created successfully.')
    return df_sorted

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host = 'localhost', port=8000, debug = True)
    # df = generate_trace(r'./LOG/tiny_sample.log')