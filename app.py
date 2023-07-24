import os
from flask import Flask, request, render_template, redirect, url_for, flash, send_file, abort
import isscam

app = Flask(__name__)

app.config['SECRET_KEY'] = "sjdcfiushfbiubfiusicfieunfjnskfncdks"

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/Inspectinator')
def home():
    return render_template('home.html')

@app.route('/Inspectinator/result', methods=["POST", "GET"])
def result():
    if request.method == "POST":
        url_input = request.form["url_input"]
        isscam.check_all_parameters(url_input)
        messages = []

        if isscam.SUS_SCORE > 2:
            age = isscam.age(url_input)
            messages.append("Site is suspicious!")
            if age < 30:
                messages.append(f"Domain is very young, just {age} days old!")
            elif age < 60:
                messages.append(f"Domain is young, just {age} days old!")
            elif age in range(60, 300):
                messages.append(f"Domain is {age} days old.")
            
            if isscam.GOOGLE == 1:
                messages.append("Google search and result analysis, seem suspicious!")
        
        elif isscam.SUS_SCORE == 0:
            messages.append("Everthing seem fine.")
        
        else:
            messages.append("Site feels suspicious!")

        return render_template('result.html', url=url_input, messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0")