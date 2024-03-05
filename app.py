from flask import Flask, render_template
from utils.weather.weatherPass import *

app = Flask(__name__)

@app.route("/")
def home():
    
    return render_template('index.html', context=passWeatherData())

if __name__ == '__main__':
    app.run()