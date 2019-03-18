'''
Sensehat Dashboard
--------------------
Author: Owen De Waele
Modified: 03-12-2019
--------------------
Installation:
sudo pip3 -U Flask
Docs: http://flask.pocoo.org/docs/1.0/
'''
# Import the libraries
from flask import Flask, jsonify, render_template, request
from sense_hat import SenseHat
import sys
import os
import pyrebase
import time

config = {
  "apiKey": "AIzaSyBYCO3HevrkCz38GZHpdH7JShA17Kd39B4",
  "authDomain": "iotlabo5.firebaseapp.com",
  "databaseURL": "https://iotlabo5.firebaseio.com",
  "projectId": "iotlabo5",
  "storageBucket": "iotlabo5.appspot.com",
  "messagingSenderId": "7052501175"
}
firebase = pyrebase.initialize_app(config)

try:
  db = firebase.database()
  # Create an instance of flask
  app = Flask(__name__)

  # Create an instance of the sensehat
  sense = SenseHat()

  # Define the root route
  @app.route('/')
  def index():
    return 'Look the flask server is running'

  # Define the nmd route
  @app.route('/nmd')
  def nmd():
    return 'Greetings Earthlings. We are NMDrs'

  # Define the my_ip route
  @app.route('/my_ip', methods=['GET'])
  def my_ip():
    return jsonify({
      'ip': request.remote_addr
    }), 200

  # Define the api_environment route
  @app.route('/api/environment', methods=['GET'])
  def api_environment():
    environment_obj = {
      'temperature': {
        'value': round(sense.get_temperature()),
        'unit': u'C'
      },
      'humidity': {
        'value': round(sense.get_humidity()),
        'unit': u'%'
      },
      'pressure': {
        'value': round(sense.get_pressure()),
        'unit': u'mbar'
      }
    }
    return jsonify(environment_obj), 200

  # Define the api_environment route
  @app.route('/environment', methods=['GET'])
  def environment():
    environment_obj = {
      'temperature': {
        'value': round(sense.get_temperature()),
        'unit': u'C'
      },
      'humidity': {
        'value': round(sense.get_humidity()),
        'unit': u'%'
      },
      'pressure': {
        'value': round(sense.get_pressure()),
        'unit': u'mbar'
      }
    }
    return render_template('environment.html', environment=environment_obj)
  # Define the colorpicker route
  @app.route('/colorpicker', methods=['GET','POST'])

  def colorpicker():
    if request.method == 'POST':
      color_obj = {
        'value': request.form['colorField'],
      }
      checkbox = request.form.get('check')
      if checkbox:
        pickedcolor = color_obj['value'].lstrip('#')
        RGBColor = tuple(int(pickedcolor[i:i+2], 16) for i in (0, 2 ,4))
        for x in range(0,8):
          for y in range(0,8):
            sense.set_pixel(x,y,RGBColor)
      else:
        for x in range(0,8):
          for y in range(0,8):
            sense.set_pixel(x,y,0,0,0)
    else:
      color_obj = {
        'value': '#ffffff',
      }
    print(color_obj)
    return render_template('colorpicker.html', colorpicker=color_obj )
  # Main method for Flask server
  if __name__ == '__main__':
    app.run(host = '192.168.0.156', port = 8080, debug = True)
    #app.run(host = '10.5.128.6', port = 8080, debug = True)
  
except (KeyboardInterrupt, SystemExit):
	sense.clear()
	print('\n' + 'Stopped ColorPicker')
	sys.exit(0)
