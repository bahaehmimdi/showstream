from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta

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

@app.route('/current_event_show', methods=['GET'])
def current_event_show():
    now = datetime.now() + timedelta(hours=2)
    for event in events:
        event_start = datetime.fromisoformat(event['start_time'])
        event_end = datetime.fromisoformat(event['end_time'])
        if event_start <= now <= event_end:
        #    return  redirect("static/"+event["event_string"]+".mp4")
            return redirect("video/"+event["event_string"]+".mp4")
    return jsonify({'event_string': 'nothing'})
    
@app.route('/current_event', methods=['GET'])
def current_event():
    now = datetime.now()+ timedelta(hours=2)
    for event in events:
        event_start = datetime.fromisoformat(event['start_time'])
        event_end = datetime.fromisoformat(event['end_time'])
        if event_start <= now <= event_end:
            event['now']=str(now)
            return jsonify(event)
    return jsonify({'event_string': 'nothing at'+now.isoformat()})

@app.route('/display', methods=['GET'])
def display():
    return render_template('display.html')
@app.route('/clear', methods=['GET'])
def clear():
    events.clear()
    return "cleared"

@app.route('/video/<video_filename>')
def video(video_filename):
   try: 
    video_path = f"http://diapo.pythonanywhere.com/static/{video_filename}"#f"https://showstream-32id.onrender.com/static/{video_filename}"
    return redirect(video_path)#render_template('video.html', video_path=video_path.replace("/video",""), audio_path=video_path.replace("/video","").replace("mp4","mp3"))
   except Exception as bahae:
       return str(bahae)
 
if __name__ == '__main__':
    app.run(debug=True)
