from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
import datetime

app = Flask(__name__)

# In-memory storage
data = {}

def get_today_date():
    return datetime.date.today().strftime("%Y-%m-%d")

@app.route('/')
def index():
    today = get_today_date()
    today_data = data.get(today, [])
    total = sum(item['price'] for item in today_data)
    return render_template('expenses.html', data=today_data, total=total, today=today, all_data=data)

@app.route('/add', methods=['POST'])
def add_expense():
    today = get_today_date()
    if today not in data:
        data[today] = []

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak your expenses (e.g., pizza 50 coffee 30):")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("🗣 You said:", text)

        words = text.split()
        i = 0
        while i < len(words) - 1:
            try:
                item = words[i]
                price = int(words[i + 1])
                data[today].append({"item": item, "price": price})
                i += 2
            except ValueError:
                i += 1
    except Exception as e:
        print("Error recognizing speech:", e)

    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_expense(index):
    today = get_today_date()
    if today in data and 0 <= index < len(data[today]):
        del data[today][index]
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
