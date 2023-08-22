from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory database for simplicity
events = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        event_string = request.form.get('event_string')
        events.append({
            'start_time': start_time,
            'end_time': end_time,
            'event_string': event_string
        })
        return redirect(url_for('index'))
    return render_template('index.html', events=events)

@app.route('/current_event', methods=['GET'])
def current_event():
    now = datetime.now().isoformat()
    for event in events:
        if event['start_time'] <= now <= event['end_time']:
            return jsonify(event)
    return jsonify({'event_string': 'nothing'})

@app.route('/display', methods=['GET'])
def display():
    return render_template('display.html')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
