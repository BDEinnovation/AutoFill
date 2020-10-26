from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os

app = Flask(__name__)

def template(title = "Dutch Brothers Store #xxxx", text = ""):
    now = datetime.datetime.now().strftime("%m-%d-%Y, %I:%M %p")
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    status = water.distance()
    message = ""
    if (status <10):
        message = "Low Level, Fill Now"
    else:
        message = "Filled"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/water")
def action2():
    water.pump1_on()
    water.pump2_on()
    templateData = template(text = "Primed")
    return render_template('main.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Autofill On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3.7 auto_water.py&")
    else:
        templateData = template(text = "Autofill Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **templateData)

@app.route("/clean")
def action3():
    water.clean_on()
    templateData = template(text = "Cleaned")
    return render_template('main.html', **templateData)

@app.route("/last_cleaned")
def check_last_cleaned():
    templateData = template(text = water.get_last_cleaned())
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='192.168.1.163', port=8080, debug=True)