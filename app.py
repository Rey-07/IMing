from flask import Flask, render_template
import json
from datetime import datetime, timezone, timedelta
import os

app = Flask(__name__)

def convert_to_ist(timestamp):
    utc_time = datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)
    ist = utc_time.astimezone(timezone(timedelta(hours=5, minutes=30)))  # IST is UTC+5:30
    return ist.strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp as needed

@app.route('/')
def display_messages():
    messages = []
    file_path = 'C:\\Users\\Dell\\OneDrive\\Desktop\\DSA\\data\\message_1.json'  # Replace with your file path
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for message in data['messages']:
            if 'sender_name' in message and 'content' in message and 'timestamp_ms' in message:
                participant_name = message['sender_name']
                message_content = message['content']
                timestamp = message['timestamp_ms']

                ist_timestamp = convert_to_ist(timestamp)

                formatted_message = {
                    'sender': participant_name,
                    'content': message_content,
                    'timestamp': ist_timestamp
                }
                messages.append(formatted_message)

        messages.reverse()  # Reverse the order of messages (most recent messages first)

    return render_template('chat.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

